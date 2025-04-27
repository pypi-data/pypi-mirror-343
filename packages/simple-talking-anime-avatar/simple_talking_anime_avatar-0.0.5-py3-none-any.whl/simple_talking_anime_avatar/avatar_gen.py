import pathlib

import cv2
import numpy as np


def overlay_transparent(background, overlay, x, y):
    """_summary_

    Args:
        background (_type_): _description_
        overlay (_type_): _description_
        x (_type_): _description_
        y (_type_): _description_

    Returns:
        _type_: _description_
    """
    background_width = background.shape[1]
    background_height = background.shape[0]

    if x >= background_width or y >= background_height:
        return background

    h, w = overlay.shape[0], overlay.shape[1]

    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype=overlay.dtype)
                * 255,
            ],
            axis=2,
        )

    overlay_image = overlay[..., :4]
    mask = overlay[..., 3:] / 255.0

    background[y : y + h, x : x + w] = (1.0 - mask) * background[
        y : y + h, x : x + w
    ] + mask * overlay_image

    return background


def get_filename(letters: str = "bb"):
    """_summary_

    Args:
        letters (str, optional): _description_. Defaults to "bb".

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """
    two_letter_match = {
        "th": "mouth_th.png",
        "ee": "mouth_ee.png",
        "ch": "mouth_chjsh.png",
        "sh": "mouth_chjsh.png",
    }
    one_letter_match = {
        "a": "mouth_aei.png",
        "b": "mouth_bmp.png",
        "c": "mouth_cdgknstxyz.png",
        "d": "mouth_cdgknstxyz.png",
        "e": "mouth_aei.png",
        "f": "mouth_fv.png",
        "g": "mouth_cdgknstxyz.png",
        "h": "mouth_chjsh.png",
        "i": "mouth_chjsh.png",
        "j": "mouth_chjsh.png",
        "k": "mouth_cdgknstxyz.png",
        "l": "mouth_l.png",
        "m": "mouth_bmp.png",
        "n": "mouth_cdgknstxyz.png",
        "o": "mouth_o.png",
        "p": "mouth_bmp.png",
        "q": "mouth_wq.png",
        "r": "mouth_r.png",
        "s": "mouth_cdgknstxyz.png",
        "t": "mouth_cdgknstxyz.png",
        "u": "mouth_u.png",
        "v": "mouth_fv.png",
        "w": "mouth_wq.png",
        "x": "mouth_cdgknstxyz.png",
        "y": "mouth_cdgknstxyz.png",
        "z": "mouth_cdgknstxyz.png",
    }
    if not letters or letters[0] in [" ", ".", ",", "'", "\n", "\t", "-", "?", "!"]:
        return one_letter_match["b"]
    if letters in two_letter_match.keys():
        return two_letter_match[letters]
    elif letters[0] in one_letter_match.keys():
        return one_letter_match[letters[0]]
    else:
        raise Exception(f"No match for {letters}")


def get_image_speaking(letters: str = "bb"):

    curr_dir_path = pathlib.Path(__file__).parent.resolve()

    mouth_filename = get_filename(letters=letters)

    background = cv2.imread(
        curr_dir_path / pathlib.Path("character_images/female1/main_image.png"),
        cv2.IMREAD_UNCHANGED,
    )
    overlay = cv2.imread(
        curr_dir_path / pathlib.Path(f"character_images/female1/{mouth_filename}"),
        cv2.IMREAD_UNCHANGED,
    )
    overlay = cv2.resize(overlay, (140, 140))

    mouth_x = 450
    mouth_y = 570

    res = overlay_transparent(
        background,
        overlay,
        int(mouth_x - overlay.shape[0] / 2),
        int(mouth_y - overlay.shape[1] / 2),
    )

    if res.shape[2] == 4:
        # Create a new image without the alpha channel
        res_rgb = cv2.cvtColor(res, cv2.COLOR_RGBA2RGB)
    else:
        # If the image doesn't have an alpha channel, keep it as is
        res_rgb = res

    return res_rgb


# dummy commit 5
