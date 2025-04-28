### Overview
We propose a flexible conditional modeling framework that learns structured dependencies between variables by blending linear and nonlinear transformations. Our method dynamically adjusts to data characteristics via a learnable mixture parameter, allowing the model to preserve simplicity where appropriate while capturing complex behaviors when necessary. We validate the approach on synthetic nonlinear datasets, achieving significant improvements over traditional linear models. This framework opens the door for scalable integration into large models, including language model retraining where structured paths in latent space matter.

### Usage
``` python
from kln import FlexibleConditional

model = FlexibleConditional(input_dim=2, hidden_dim=64, output_dim=1)
```

### Acknowledgements
OpenAI's ChatGPT provided substantial assistance with the research, writing, and development of this work. The authors gratefully acknowledge its contributions while assuming full responsibility for the final content.

We thank the contributors to open-source geometry libraries and acknowledge the support of interdisciplinary visualization research.

We would also like to include [this poem](https://github.com/michalkrupa/kln/blob/main/FlexibleConditionalPaper/poem.md), written by ChatGPT o4
#### REFERENCES
[1] J. A. Reeds and L. A. Shepp. 1990. Optimal paths for a car that goes both forwards and backwards. Pacific J. Math. 145, 2 (1990), 367–393.

[2] Michal Krupa. 2025. Geometrically-Constrained Pathfinding: An Arc-Based Algorithm for Navigation in Restricted Domains. In . ACM, New York, NY, USA, 1 page.
