# Graduate Project Notes

## Suggested research framing

**Title:** A Python-Based Operations Research Toolkit for Industrial Logistics Optimization and Resource Allocation

### Research components

1. LP production/resource allocation model.
2. Transportation model with multiple construction heuristics.
3. MODI transportation-simplex improvement procedure.
4. Assignment optimization using the Hungarian algorithm.
5. Stochastic demand scenario generation.
6. Comparative computational experiments.

### What makes the implementation substantially richer than a two-variable demo

- Explicit mathematical model objects.
- Independent algorithm modules.
- Multiple transportation heuristics and an optimization phase.
- Cross-validation between an educational simplex and HiGHS.
- Feasibility and binding-constraint diagnostics.
- Uncertainty analysis.
- Reproducible datasets.
- Unit testing.
- Command-line execution.
- Packaging metadata.

### Recommended thesis methodology

For an actual master's study, collect real industrial observations, define the decision variables and objective function from the organization, estimate or validate costs and capacities, clean and anonymize the dataset, calibrate the model, compare algorithms, perform sensitivity/scenario analysis, and validate the recommendations with operational stakeholders. The included data are examples and should not be represented as proprietary Ahmedabad industrial data.
