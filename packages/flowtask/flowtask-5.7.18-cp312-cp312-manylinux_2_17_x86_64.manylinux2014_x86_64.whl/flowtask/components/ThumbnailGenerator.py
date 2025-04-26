from typing import Callable
import asyncio
import os
from pathlib import Path
from io import BytesIO
from PIL import Image
import pandas as pd
from .flow import FlowComponent


class ThumbnailGenerator(FlowComponent):
    """
    ThumbnailGenerator.

        Overview
        This component generates thumbnails for images stored in a DataFrame. It takes an image column, resizes the images
        to a specified size, and saves them in a specified directory with a given filename format. The generated thumbnail
        paths are added to a new column in the DataFrame.
        .. table:: Properties
        :widths: auto
        +----------------+----------+-----------+---------------------------------------------------------------+
        | Name           | Required | Summary                                                                   |
        +----------------+----------+-----------+---------------------------------------------------------------+
        | data_column    |   Yes    | The name of the column containing the image data.                       |
        +----------------+----------+-----------+---------------------------------------------------------------+
        | thumbnail_column|  Yes    | The name of the column to store the generated thumbnail paths.         |
        +----------------+----------+-----------+---------------------------------------------------------------+
        | size           |   Yes    | The size of the thumbnail. Can be a tuple (width, height) or a single |
        |                |          | integer for a square thumbnail.                                     |
        +----------------+----------+-----------+---------------------------------------------------------------+
        | format         |   Yes    | The format of the thumbnail (e.g., 'JPEG', 'PNG').                    |
        +----------------+----------+-----------+---------------------------------------------------------------+
        | directory      |   Yes    | The directory where the thumbnails will be saved.                     |
        +----------------+----------+-----------+---------------------------------------------------------------+
        | filename       |   Yes    | The filename template for the thumbnails. It can include placeholders  |
        |                | for DataFrame columns (e.g., '{column_name}.jpg').                    |
        +----------------+----------+-----------+---------------------------------------------------------------+
        Returns
        This component returns a DataFrame with a new column containing the paths of the generated thumbnails.
        Example:
        ```
        - ThumbnailGenerator:
            data_column: image
            thumbnail_column: thumbnail
            size: (128, 128)
            format: JPEG
            directory: /path/to/thumbnails
            filename: thumbnail_{id}.jpg
        ```
    """  # noqa: E501
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.data_column = kwargs.pop("data_column", None)
        self.thumbnail_column = kwargs.pop("thumbnail_column", 'thumbnail')
        if not self.data_column:
            raise ValueError("data_column must be specified.")
        self.size = kwargs.pop("size", (128, 128))
        self.size = self.size if isinstance(self.size, tuple) else (self.size, self.size)
        self.format = kwargs.pop("format", "JPEG").upper()
        self.directory = kwargs.pop("directory", "./thumbnails")
        self.filename_template = kwargs.pop("filename", "thumbnail_{id}.jpg")
        super(ThumbnailGenerator, self).__init__(loop=loop, job=job, stat=stat, **kwargs)
        self._semaphore = asyncio.Semaphore(10)  # Adjust the limit as needed

    async def start(self, **kwargs) -> bool:
        if self.previous:
            self.data = self.input
        if isinstance(self.directory, str):
            self.directory = Path(self.directory).resolve()
        # check if directory exists
        if self.directory.exists() and not self.directory.is_dir():
            raise ValueError(f"{self.directory} is not a directory.")
        if not self.directory.exists():
            self.directory.mkdir(parents=True, exist_ok=True)
        return True

    async def close(self):
        return True

    async def run(self) -> pd.DataFrame:
        # check for duplicates
        async def handle(idx):
            async with self._semaphore:
                row = self.data.loc[idx].to_dict()
                file_obj = row[self.data_column]
                if file_obj:
                    image = Image.open(BytesIO(file_obj.getvalue()))
                    image.thumbnail(self.size)
                    filename = self.filename_template.format(**row)
                    filepath = self.directory.joinpath(filename)
                    # Set the thumbnail path in the DataFrame
                    self.data.at[idx, self.thumbnail_column] = str(filepath)
                    # check if file exists
                    if filepath.exists():
                        return
                    image.save(filepath, self.format)

        await asyncio.gather(*(handle(i) for i in self.data.index))

        self._result = self.data
        return self._result
