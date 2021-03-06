{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "Test ",
      "provenance": [],
      "authorship_tag": "ABX9TyO+U6YaX5tgqohn6lXGSf0t",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/ViktoryiaStrylets/Test-/blob/master/Test.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "_ym7HuBBo866",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "\n",
        "def get_face_embedding(data, context):\n",
        "\n",
        "  %tensorflow_version 1.x\n",
        "  import tensorflow as tf\n",
        "  import matplotlib.pyplot as plt\n",
        "  from PIL import Image\n",
        "  from numpy import asarray\n",
        "  from numpy import expand_dims\n",
        "  from scipy.spatial.distance import cosine\n",
        "  from mtcnn.mtcnn import MTCNN\n",
        "  from keras_vggface.vggface import VGGFace\n",
        "  from keras_vggface.utils import preprocess_input\n",
        "  import cv2\n",
        "  # Import Libraries\n",
        "  import pyrebase\n",
        "  import os\n",
        "  import tempfile\n",
        "\n",
        "  from google.cloud import storage\n",
        "  from wand.image import Image\n",
        "\n",
        "  storage_client = storage.Client()\n",
        "  config = {\n",
        "       \"apiKey\": \"AIzaSyBzzo7YG-4JSn7OwxQVLpTO6f6QjBy7o40\",\n",
        "       \"authDomain\": \"sci-match.firebaseapp.com\",\n",
        "       \"databaseURL\": \"https://sci-match.firebaseio.com\",\n",
        "       \"storageBucket\": \"sci-match.appspot.com\"\n",
        "       }\n",
        "  firebase = pyrebase.initialize_app(config)\n",
        "  file_data = data\n",
        "\n",
        "  file_name = file_data['name']\n",
        "  bucket_name = file_data['bucket']\n",
        "\n",
        "  blob = storage_client.bucket(bucket_name).get_blob(file_name)\n",
        "  blob_uri = f'gs://{bucket_name}/{file_name}'\n",
        "  blob_source = {'source': {'image_uri': blob_uri}}\n",
        "  file_name = blob.name\n",
        "  temp_local_filename = tempfile.mkstemp()\n",
        "  # Download file from bucket.\n",
        "  filename = blob.download_to_filename(temp_local_filename)\n",
        "\n",
        "\t# load image from file\n",
        "  pixels = cv2.imread(filename) \n",
        "\t# create the detector, using default weights\n",
        "  detector = MTCNN()\n",
        "\t# detect faces in the image\n",
        "  results = detector.detect_faces(pixels)\n",
        "\t# extract the bounding box from the first face\n",
        "  x1, y1, width, height = results[0]['box']\n",
        "  x2, y2 = x1 + width, y1 + height\n",
        "\t# extract the face\n",
        "  face = pixels[y1:y2, x1:x2]\n",
        "\t# resize pixels to the model size\n",
        "  image = Image.fromarray(face)\n",
        "  image = image.resize((224, 224))\n",
        "  face_array = asarray(image)\n",
        "  \n",
        "  sample = asarray(face_array, 'float32')\n",
        "  sample = expand_dims(sample, axis=0)\n",
        "\t# prepare the face for the model, e.g. center pixels\n",
        "  sample = preprocess_input(sample, version=2)\n",
        "\t# create a vggface model\n",
        "  model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')\n",
        "\t# perform prediction\n",
        "  yhat = model.predict(sample)\n",
        "\n",
        "  \n",
        "  db = firebase.database()\n",
        "  db.child().push(yhat)\n",
        "\n",
        "      \n",
        "  os.remove(temp_local_filename)\n",
        "\n",
        "\n"
      ],
      "execution_count": null,
      "outputs": []
    }
  ]
}
