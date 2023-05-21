## PEAK: Explainable Privacy Assistant through Automated Knowledge Extraction <br>
PEAK is a privacy assistant that explains privacy labels by generating human-understandable explanations. PEAK is composed of the following five stages:


<p align="center">
  <img src="https://github.com/aycignl/peak/blob/main/peak_system.png" width="800"/>
</p>

1. [[Annotated Data](https://github.com/aycignl/peak/tree/main/dataset_dir)] The starting point for PEAK is a set of labeled public and private images. The data could come from a user's own history of personal online images (i.e. both shared and not shared), or from a publicly available dataset of labeled images.<br>
2. [[Generate Tags](https://github.com/aycignl/peak/blob/main/generate_tags.py)] The second stage involves assigning tags to each image. The generated tags are in plain language such as "tree" or "baby", and they can be provided by users themselves or automatically generated by a tool such as [Clarifai](https://clarifai.com/clarifai/main/models/general-image-recognition).<br>
3. [[Explore Topics](https://github.com/aycignl/peak/blob/main/explore_topics.ipynb)] The third stage is using the set of labeled and tagged images to perform topic modelling, which is a technique used to extract latent topics from textual information (i.e. the tags).<br>
4. [[Classify Images](https://github.com/aycignl/peak/blob/main/classify_images.ipynb)] The fourth stage is to train a tree-based ML algorithm for binary image classification. Additionally, the contributions of each topic  to the privacy decision (i.e. positive or negative effect) are computed. <br>
5. [[Generate Explanations]()] The final stage is identifying explanation categories for images, which essentially are image profiles with certain characteristics in terms of topic contributions. For instance, there may be a single dominant topic that pushes the prediction overwhelmingly in one direction. Based on the topics' contributions to privacy prediction, images are assigned to one of four explanation categories we identified: Dominant, Opposing, Collaborative, and Weak. Finally, for each explanation category, there is a distinct textual and visual explanation pattern based on the image's topics and the relationships between topics.<br>

## Citations

You can read/cite our [Paper]().
