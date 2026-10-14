import numpy as np
import cv2


# RECHERCHE LOCALE
def find_locales(image, threshold = 0.9):
    """

    :param image:       Image résultante d'une corrélation
    :param threshold:   Seuil de détection des corrélations
    :return:            Liste des coordonnées (x, y, val)
    """

    # Taille du voisinage dans lequel on cherche les maximums locaux
    kernel_size = 11

    # Le kernel doit être de taille impaire
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    # Pour chaque pixel, dilate donne le maximum dans son voisinage
    local_max = cv2.dilate(image, kernel)

    # Un pixel est conservé si :
    # 1. il dépasse le seuil
    # 2. il est égal au maximum local
    mask = (
        (image >= threshold) &
        (image == local_max)
    )

    ys, xs = np.where(mask)

    matches = [
        (int(x), int(y), float(image[y, x]))
        for x, y in zip(xs, ys)
    ]
    return matches



def compute_iou(a, b):
    """IoU entre deux rectangles (x, y, w, h)."""

    ax1, ay1 = a["x"], a["y"]
    ax2, ay2 = ax1 + a["w"], ay1 + a["h"]

    bx1, by1 = b["x"], b["y"]
    bx2, by2 = bx1 + b["w"], by1 + b["h"]

    ix1 = max(ax1, bx1)
    iy1 = max(ay1, by1)
    ix2 = min(ax2, bx2)
    iy2 = min(ay2, by2)

    iw = max(0, ix2 - ix1)
    ih = max(0, iy2 - iy1)

    intersection = iw * ih

    area_a = a["w"] * a["h"]
    area_b = b["w"] * b["h"]

    union = area_a + area_b - intersection

    return intersection / union if union > 0 else 0

def find_all_matches_multiscale(
    image,
    template,
    threshold=0.9,
    max_matches=20,
    min_scale=0.5,
    max_scale=3.0,
    num_scales=25,
    iou_threshold=0.3
):
    """
    Recherche toutes les occurrences d'un template entre
    min_scale et max_scale.

    Retourne une liste triée :

        [
            {
                "x": ...,
                "y": ...,
                "w": ...,
                "h": ...,
                "score": ...,
                "scale": ...
            },
            ...
        ]
    """

    # Conversion en niveaux de gris
    if image.ndim == 3:
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        image_gray = image

    if template.ndim == 3:
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    else:
        template_gray = template

    img_h, img_w = image_gray.shape[:2]

    # Échelles géométriquement espacées
    scales = np.geomspace(
        min_scale,
        max_scale,
        num_scales
    )

    candidates = []

    for scale in scales:

        # Taille du template à cette échelle
        new_w = max(1, round(template_gray.shape[1] * scale))
        new_h = max(1, round(template_gray.shape[0] * scale))

        # Le template doit rentrer dans l'image
        if new_w > img_w or new_h > img_h:
            continue

        interpolation = (
            cv2.INTER_AREA
            if scale < 1.0
            else cv2.INTER_LINEAR
        )

        scaled_template = cv2.resize(
            template_gray,
            (new_w, new_h),
            interpolation=interpolation
        )

        # Corrélation
        result = cv2.matchTemplate(
            image_gray,
            scaled_template,
            cv2.TM_CCOEFF_NORMED
        )

        # ------------------------------------------------
        # Maximums locaux
        # ------------------------------------------------

        # Rayon approximatif pour éviter plusieurs pixels
        # correspondant à la même détection
        kernel_size = max(
            3,
            int(min(new_w, new_h) / 4)
        )

        # Kernel doit être impair
        if kernel_size % 2 == 0:
            kernel_size += 1

        kernel = np.ones(
            (kernel_size, kernel_size),
            dtype=np.uint8
        )

        local_max = cv2.dilate(result, kernel)

        mask = (
            (result >= threshold)
            & (result == local_max)
        )

        ys, xs = np.where(mask)

        for x, y in zip(xs, ys):

            candidates.append({
                "x": int(x),
                "y": int(y),
                "w": int(new_w),
                "h": int(new_h),
                "score": float(result[y, x]),
                "scale": float(scale)
            })

    # ------------------------------------------------
    # Tri global par score
    # ------------------------------------------------

    candidates.sort(
        key=lambda m: m["score"],
        reverse=True
    )

    # ------------------------------------------------
    # Non Maximum Suppression globale
    # ------------------------------------------------

    matches = []

    for candidate in candidates:

        duplicate = False

        for match in matches:

            if compute_iou(candidate, match) > iou_threshold:
                duplicate = True
                break

        if not duplicate:
            matches.append(candidate)

        if len(matches) >= max_matches:
            break

    return matches

