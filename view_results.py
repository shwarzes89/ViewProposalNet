# coding=utf-8
import os

from PIL import Image
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import project_utils
from py_utils import dir_utils, load_utils


def sort_results(data):
    points = data[0]
    score = data[1]
    width, height = points[2] - points[0], points[3] - points[1]
    ratio = float(width) / float(height)

    diff = abs((232 / 116) - ratio)

    return score / diff


def crop_resize(image, size, ratio):
    # crop to ratio, center
    w, h = image.size
    if w > ratio * h:  # width is larger then necessary
        x, y = (w - ratio * h) // 2, 0
    else:  # ratio*height >= width (height is larger)
        x, y = 0, (h - w / ratio) // 2
    image = image.crop((x, y, w - x, h - y))

    # resize
    if image.size > size:  # don't stretch smaller images
        image.thumbnail(size, Image.ANTIALIAS)
    return image


def viewBBoxes(image_file, actual_img_path, bboxes, titles, image_name):
    n_items_per_row = 4
    image_origin = Image.open(image_file)
    image = np.array(image_origin, dtype=np.uint8)
    n_crops = len(bboxes)
    n_rows = n_crops // n_items_per_row + 1

    fig = plt.figure(figsize=[20, 20])
    fig.suptitle(os.path.basename(image_file))

    results = zip(bboxes, titles)
    # results = sorted(results, key=sort_results)

    ax = fig.add_subplot(n_rows, n_items_per_row, 1)

    ax.imshow(image_origin)
    ax.set_axis_off()
    ax.set_title('original')

    croppion_area = results[-1][0]

    adjusted_thumbnail = image_origin.crop(croppion_area)
    adjusted_thumbnail.save('./auto_generated/' + image_name)
    ax = fig.add_subplot(n_rows, n_items_per_row, 2)
    ax.imshow(adjusted_thumbnail)
    ax.set_axis_off()
    ax.set_title('auto generated thumbnail')

    cropped_thumbnail = crop_resize(adjusted_thumbnail, (232, 116), 2)
    cropped_thumbnail.save('./cropped/' + image_name)
    ax = fig.add_subplot(n_rows, n_items_per_row, 3)
    ax.imshow(cropped_thumbnail)
    ax.set_axis_off()
    ax.set_title('cropped')

    # ax = fig.add_subplot(n_rows, n_items_per_row, 4)
    # ax.imshow(Image.open(actual_img_path).resize((232, 116)))
    # ax.set_axis_off()
    # ax.set_title('Stove thumbnail')

    # for idx, data in enumerate(results):
    #     s_bbox = data[0]
    #     title = data[1]
    #
    #     ax = fig.add_subplot(n_rows, n_items_per_row, idx + 1)
    #     ax.imshow(image)
    #     ax.set_axis_off()
    #
    #     width, height = s_bbox[2] - s_bbox[0], s_bbox[3] - s_bbox[1]
    #
    #     ax.set_title(title)
    #
    #     rect_i = patches.Rectangle((s_bbox[0], s_bbox[1]), width, height,
    #                                linewidth=2, edgecolor='yellow', facecolor='none')
    #
    #     # Add the patch to the Axes
    #     ax.add_patch(rect_i)

    plt.show(block=False)
    raw_input("Press Enter to continue...")
    plt.close()


annotation_path = 'ProposalResults/ViewProposalResults-tmp.txt'
image_path_root = './example_stoves'
actual_img_path = './actual'

image_data = load_utils.load_json(annotation_path)
image_name_list = image_data.keys()
image_name_list.sort()
for idx, image_name in enumerate(image_name_list):
    s_image_path = os.path.join(image_path_root, image_name)
    a_img_path = os.path.join(actual_img_path, image_name)

    bboxes = image_data[image_name]['bboxes']
    scores = image_data[image_name]['scores']
    viewBBoxes(s_image_path, a_img_path, bboxes, scores, image_name)

print "DEBUG"
