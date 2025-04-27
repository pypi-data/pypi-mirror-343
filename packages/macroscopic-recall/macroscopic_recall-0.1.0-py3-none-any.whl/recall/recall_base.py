#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : yanpei.fan@centurygame.com
# @Date: 2025/4/27-14:06
# @Desc    :


import json as _json
import csv as _csv
from pathlib import Path as _Path


class Recall(object):

    support_file_type = ["json", "csv"]

    @classmethod
    def handle_file2md(cls, file_path: _Path):
        file_type = file_path.suffix[1:]
        if hasattr(cls, f"_{file_type}2entries"):
            entries = getattr(cls, f"_{file_type}2entries")(file_path)
            return cls._convert_entries_to_md(file_path.stem, entries)
        raise ValueError(f"Unsupported file type: {file_type}, only support {cls.support_file_type}")

    @classmethod
    def _csv2entries(cls, file_path):
        result = []
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = _csv.reader(f)
            for index, row in enumerate(reader):
                if index == 0:
                    filed_row = row
                    continue
                real_row = {}
                for cell_index, cell in enumerate(row):
                    if cell_index == 0:
                        real_row.setdefault("__title__", cell)
                    else:
                        real_row[filed_row[cell_index]] = cell
                result.append(real_row)
            return result

    @classmethod
    def _json2entries(cls, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = _json.load(f)
        if not isinstance(data, list):
            raise ValueError("JSON must be a list of dicts")
        entries = []
        for item in data:
            if not isinstance(item, dict):
                continue
            for title, detail in item.items():
                if isinstance(detail, dict):
                    entries.append({"__title__": title, **detail})
        return entries

    @classmethod
    def _convert_entries_to_md(cls, name, entries):
        md = f"{'-' * 20}\n{name}\n{'-' * 20}\n\n"
        for entry in entries:
            title = entry.get("__title__") or list(entry.keys())[0]
            md += f"# {title}\n"
            for key, value in entry.items():
                if key == "__title__" or key == title:
                    continue
                md += f"## {key}\n"
                if isinstance(value, str) and ("、" in value or "，" in value):
                    parts = [v.strip() for v in value.replace("，", "、").split("、")]
                    for part in parts:
                        md += f"- {part}\n"
                else:
                    md += f"- {value}\n"
            md += "\n"
        return md.strip()