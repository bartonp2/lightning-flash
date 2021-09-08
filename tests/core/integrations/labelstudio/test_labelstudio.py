from flash.text.classification.data import TextClassificationData

from flash.video.classification.data import VideoClassificationPreprocess, VideoClassificationData

from data.data_source import DefaultDataSources
from flash.core.integrations.labelstudio.data_source import LabelStudioDataSource, \
    LabelStudioImageClassificationDataSource, LabelStudioTextClassificationDataSource
from flash.core.data.utils import download_data
from image import ImageClassificationData


def test_utility_load():
    """Test for label studio json loader."""
    data = [
        {
            "id": 191,
            "annotations": [
                {
                    "id": 130,
                    "completed_by": {"id": 1, "email": "test@heartex.com", "first_name": "", "last_name": ""},
                    "result": [
                        {
                            "id": "dv1Tn-zdez",
                            "type": "rectanglelabels",
                            "value": {
                                "x": 46.5625,
                                "y": 21.666666666666668,
                                "width": 8.75,
                                "height": 12.083333333333334,
                                "rotation": 0,
                                "rectanglelabels": ["Car"],
                            },
                            "to_name": "image",
                            "from_name": "label",
                            "image_rotation": 0,
                            "original_width": 320,
                            "original_height": 240,
                        },
                        {
                            "id": "KRa8jEvpK0",
                            "type": "rectanglelabels",
                            "value": {
                                "x": 66.875,
                                "y": 22.5,
                                "width": 14.0625,
                                "height": 17.5,
                                "rotation": 0,
                                "rectanglelabels": ["Car"],
                            },
                            "to_name": "image",
                            "from_name": "label",
                            "image_rotation": 0,
                            "original_width": 320,
                            "original_height": 240,
                        },
                        {
                            "id": "kAKaSxNnvH",
                            "type": "rectanglelabels",
                            "value": {
                                "x": 93.4375,
                                "y": 22.916666666666668,
                                "width": 6.5625,
                                "height": 18.75,
                                "rotation": 0,
                                "rectanglelabels": ["Car"],
                            },
                            "to_name": "image",
                            "from_name": "label",
                            "image_rotation": 0,
                            "original_width": 320,
                            "original_height": 240,
                        },
                        {
                            "id": "_VXKV2nz14",
                            "type": "rectanglelabels",
                            "value": {
                                "x": 0,
                                "y": 39.583333333333336,
                                "width": 100,
                                "height": 60.416666666666664,
                                "rotation": 0,
                                "rectanglelabels": ["Road"],
                            },
                            "to_name": "image",
                            "from_name": "label",
                            "image_rotation": 0,
                            "original_width": 320,
                            "original_height": 240,
                        },
                        {
                            "id": "vCuvi_jLHn",
                            "type": "rectanglelabels",
                            "value": {
                                "x": 0,
                                "y": 17.5,
                                "width": 48.125,
                                "height": 41.66666666666666,
                                "rotation": 0,
                                "rectanglelabels": ["Obstacle"],
                            },
                            "to_name": "image",
                            "from_name": "label",
                            "image_rotation": 0,
                            "original_width": 320,
                            "original_height": 240,
                        },
                    ],
                    "was_cancelled": False,
                    "ground_truth": False,
                    "prediction": {},
                    "result_count": 0,
                    "task": 191,
                }
            ],
            "file_upload": "Highway20030201_1002591.jpg",
            "data": {"image": "/data/upload/Highway20030201_1002591.jpg"},
            "meta": {},
            "created_at": "2021-05-12T18:43:41.241095Z",
            "updated_at": "2021-05-12T19:42:28.156609Z",
            "project": 7,
        }
    ]
    ds = LabelStudioDataSource._load_json_data(data=data, data_folder=".", multi_label=False)
    assert ds[3] == {"image"}
    assert ds[2] == {"Road", "Car", "Obstacle"}
    assert len(ds[1]) == 0
    assert len(ds[0]) == 5
    ds_multi = LabelStudioDataSource._load_json_data(data=data, data_folder=".", multi_label=True)
    assert ds_multi[3] == {"image"}
    assert ds_multi[2] == {"Road", "Car", "Obstacle"}
    assert len(ds_multi[1]) == 0
    assert len(ds_multi[0]) == 5


def test_datasource_labelstudio():
    """
    Test creation of LabelStudioDataSource
    """
    download_data("https://label-studio-testdata.s3.us-east-2.amazonaws.com/lightning-flash/data.zip")
    ds = LabelStudioDataSource()
    data = {
        "data_folder": "data/upload/",
        "export_json": "data/project.json",
        "split": 0.2,
        "multi_label": False,
    }
    train, val, test, predict = ds.to_datasets(train_data=data)
    sample = train[0]
    assert sample
    ds_no_split = LabelStudioDatsaSource()
    data = {
        "data_folder": "data/upload/",
        "export_json": "data/project.json",
        "multi_label": True,
    }
    train, val, test, predict = ds_no_split.to_datasets(train_data=data)
    sample = train[0]
    assert sample


def test_datasource_labelstudio_image():
    """
    Test creation of LabelStudioImageClassificationDataSource and Datamodule from images
    """
    download_data("https://label-studio-testdata.s3.us-east-2.amazonaws.com/lightning-flash/data.zip")

    data = {
        "data_folder": "data/upload/",
        "export_json": "data/project.json",
        "split": 0.2,
        "multi_label": False,
    }
    ds = LabelStudioImageClassificationDataSource()
    train, val, test, predict = ds.to_datasets(train_data=data, val_data=data, test_data=data, predict_data=data)
    train_sample = train[0]
    val_sample = val[0]
    test_sample = test[0]
    predict_sample = predict[0]
    assert train_sample
    assert val_sample
    assert test_sample
    assert predict_sample

    datamodule = ImageClassificationData.from_labelstudio(
        export_json="data/project.json",
        data_folder="data/upload/",
        val_split=0.5,
    )
    assert datamodule


def test_datasource_labelstudio_text():
    """
    Test creation of LabelStudioTextClassificationDataSource and Datamodule from text
    """
    download_data("https://label-studio-testdata.s3.us-east-2.amazonaws.com/lightning-flash/text_data.zip", "./data/")
    backbone = "prajjwal1/bert-medium"
    data = {
        "data_folder": "data/upload/",
        "export_json": "data/project.json",
        "split": 0.2,
        "multi_label": False,
    }
    ds = LabelStudioTextClassificationDataSource(backbone=backbone)
    train, val, test, predict = ds.to_datasets(train_data=data, test_data=data)
    train_sample = train[0]
    test_sample = test[0]
    val_sample = val[0]

    assert train_sample
    assert test_sample
    assert val_sample

    datamodule = TextClassificationData.from_labelstudio(
        export_json="data/project.json",
        val_split=0.2,
        backbone=backbone,
    )
    assert datamodule


def test_datasource_labelstudio_video():
    """
    Test creation of Datamodule from video
    """
    download_data("https://label-studio-testdata.s3.us-east-2.amazonaws.com/lightning-flash/video_data.zip")

    data = {
        "data_folder": "data/upload/",
        "export_json": "data/project.json",
        "multi_label": True
    }
    preprocess = VideoClassificationPreprocess()
    ds = preprocess.data_source_of_name(DefaultDataSources.LABELSTUDIO)

    train, val, test, predict = ds.to_datasets(train_data=data, test_data=data)

    assert train
    assert test

    datamodule = VideoClassificationData.from_labelstudio(
        export_json="data/project.json",
        data_folder="data/upload/",
        val_split=0.2,
        clip_sampler="uniform",
        clip_duration=1,
        decode_audio=False,
    )
    assert datamodule