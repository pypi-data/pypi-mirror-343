# DynBenchmark

[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://dyn-benchmark.readthedocs.io/en/latest//)
[![License](https://img.shields.io/badge/License-EUPL%20v1.2-blue.svg)](https://joinup.ec.europa.eu/page/eupl-text-11-12)

## Customizable Ground Truths to Benchmark Community Detection and Tracking in Temporal Networks

![Sankey diagram showing community evolution](doc/_static/sankey_example.png)

DynBenchmark is a comprehensive toolkit for generating customizable ground truths to benchmark community detection and tracking algorithms in temporal networks.

## 🚀 Key Features

- **Ground Truth Generation**: Create customizable evolving communities that can grow, shrink, merge, split, appear, or disappear.
- **Comprehensive Metrics**: Analyze networks and communities with rich metrics for structures and evolution patterns.
- **Visualization Tools**: Understand community dynamics with intuitive visualizations and interactive diagrams.
- **Algorithm Evaluation**: Compare detection algorithms against ground truth with specialized metrics.

## 🏁 Quick Start

```python
# Install the package
pip install dyn-benchmark[pretty]
   
# Generate a customized benchmark
from dyn.benchmark.generator.groundtruth_generator import GroundtruthGenerator
   
# Create a generator with specific parameters
generator = GroundtruthGenerator(seed=42)
   
# Generate the benchmark with evolving communities
groundtruth = generator.generate()
   
# Visualize community evolution with Sankey diagram
from dyn.drawing.sankey_drawing import plot_sankey
from dyn.core.communities import Membership
   
membership = Membership.from_tcommlist(groundtruth.tcommlist)
plot_sankey(membership.community_graph)
```

**[See our full documentation](https://dyn-benchmark.readthedocs.io/en/latest//)** for detailed tutorials, additional examples and a full API reference.

## 📝 Citation

If you use DynBenchmark in your research, please use the following BibTeX entry:

```
Brisson, L., Bothorel, C., & Duminy, N. (2025). DynBenchmark: Customizable Ground 
Truths to Benchmark Community Detection and Tracking in Temporal Networks, France's International Conference on Complex Systems (FRCCS 2025), Bordeaux, France
```

BibTeX:

```bibtex
@inproceedings{brisson2025dynbenchmark,
  title={DynBenchmark: Customizable Ground Truths to Benchmark Community Detection and Tracking in Temporal Networks},
  author={Brisson, Laurent and Bothorel, Cécile and Duminy, Nicolas},
  booktitle={France's International Conference on Complex Systems},
  year={2025},
  publisher={Springer}
}
```

## 👥 Contributing

This package is growing continuously and contributions are welcomed.
Contributions can come in the form of new features, bug fixes, documentation improvements
or any combination thereof.

If you want to contribute to this package, please read the [Contributing guidelines](https://gitlab.com/decide.imt-atlantique/dyn/benchmark/-/blob/main/doc/contributing).
If you have any new ideas or have found bugs, feel free to [create an issue](https://gitlab.com/decide.imt-atlantique/dyn/benchmark/-/issues/new).
Finally, any contribution must be proposed for integration as a [Merge Request](https://gitlab.com/decide.imt-atlantique/dyn/benchmark/-/merge_requests/new).

Please visit our [Gitlab](https://gitlab.com/decide.imt-atlantique/dyn/benchmark) for more details.

## 📄 License

This software is licensed under the [European Union Public Licence (EUPL) v1.2](https://joinup.ec.europa.eu/page/eupl-text-11-12).
For more information see [this](https://gitlab.com/decide.imt-atlantique/dyn/benchmark/-/blob/main/LICENSE).