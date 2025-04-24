def get_okko_card(text: str, deep_link: str) -> dict:
    return {
        "card": {
            "type": "list_card",
            "cells": [
                {
                    "type": "left_right_cell_view",
                    "left": {
                        "type": "simple_left_view",
                        "icon": {
                            "tint_color": "solid_brand",
                            "address": {
                                "type": "local",
                                "identificator": "other",
                            },
                            "size": {"width": "medium", "height": "medium"},
                            "margins": {
                                "left": "8x",
                                "top": "5x",
                                "right": "6x",
                                "bottom": "5x",
                            },
                        },
                        "title": {
                            "text": text,
                            "typeface": "body1",
                            "text_color": "default",
                            "max_lines": 1,
                            "margins": {"top": "9x", "bottom": "9x"},
                        },
                    },
                    "right": {
                        "type": "disclosure_right_view",
                        "margins": {
                            "top": "8x",
                            "right": "4x",
                            "bottom": "8x",
                        },
                    },
                    "actions": [{"type": "deep_link", "deep_link": deep_link}],
                }
            ],
        }
    }
