import unittest
import itertools
import flowpaths as fp

# Run as `python -m tests.test_kmpe` in the `flowpaths` directory


class TestkMinPathError(unittest.TestCase):

    def setUp(self):
        weight_type = [float]  # 0
        optimize_with_safe_paths = [True, False]  # 1
        optimize_with_safe_sequences = [True, False]  # 2
        optimize_with_safe_zero_edges = [True, False]  # 3
        solvers = ["highs", "gurobi"]  # 4

        self.graphs = fp.graphutils.read_graphs("./tests/tests.graph")
        self.params = list(
            itertools.product(
                weight_type,
                optimize_with_safe_paths,
                optimize_with_safe_sequences,
                optimize_with_safe_zero_edges,
                solvers,
            )
        )

    def test_min_flow_decomp_solved(self):

        for graph in self.graphs:

            print("Testing graph: ", graph.graph["id"])
            stG = fp.stDiGraph(graph)
            num_paths = stG.get_width()

            first_solution_size = None

            for settings in self.params:
                # safe paths and safe sequences cannot be both True
                if settings[1] == True and settings[2] == True:
                    continue
                # we don't allow safe paths and safe sequences both False
                if (
                    settings[1] == False
                    and settings[2] == False
                ):
                    continue
                # if optimize_with_greedy, it makes no sense to try the safety optimizations
                if settings[4] == True and (
                    settings[2] == True or settings[3] == True or settings[4] == True
                ):
                    continue

                optimization_options = {
                    "optimize_with_safe_paths": settings[1],
                    "optimize_with_safe_sequences": settings[2],
                    "optimize_with_safe_zero_edges": settings[3],
                }

                solver_options = {"external_solver": settings[4]}

                kmpe_model = fp.kMinPathError(
                    graph,
                    flow_attr="flow",
                    k=num_paths,
                    weight_type=settings[0],
                    optimization_options=optimization_options,
                    solver_options=solver_options,
                )
                kmpe_model.solve()
                # print(kmpe_model.kwargs)
                print(settings)
                print(kmpe_model.solve_statistics)
                self.assertTrue(kmpe_model.is_solved(), "Model should be solved")
                self.assertTrue(
                    kmpe_model.is_valid_solution(),
                    "The solution is not a valid flow decomposition, under the default tolerance.",
                )
                self.assertTrue(
                    kmpe_model.verify_edge_position(),
                    "The MILP encoded edge positions (inside paths) are not correct.",
                )

                current_solution = kmpe_model.get_solution()
                if first_solution_size == None:
                    first_solution_size = len(current_solution["paths"])
                else:
                    self.assertEqual(
                        first_solution_size,
                        len(current_solution["paths"]),
                        "The size of the solution should be the same for all settings.",
                    )


if __name__ == "__main__":
    unittest.main()
