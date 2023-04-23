# Python standard library
from typing import Any
from typing import Dict
from typing import Tuple

# Pillow imports
from PIL import Image
# Instagram models
from instagram.posts.models import Post


def post_images(**kwargs: Dict[str, Any]) -> None:
    img = Image.open(kwargs['image'])