'''
The main file for APAD Project 1

Author: Tianyi (Kelly) Zhang
        Shikha Singh

Creation Date: 07/21/2019

Major: MSITM
'''

import utils
from admin import Admin


def main():
    print("APAD Project 1 main()!!!!!!!")

    id_num = utils.generate_id_for_role()
    print(id_num)


if __name__ == '__main__':
    main()
