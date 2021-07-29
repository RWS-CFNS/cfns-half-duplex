#!/usr/bin/python

class Folder:
    def __init__(self, path):
        self.path = path
        self.files = []

    def get_path(self):
        return self.path

    def set_path(self, new_path):
        self.path = new_path

    def get_list_files(self):
        return self.files

    # def set_list_files(self):
    #     files = []
    #     for x in os.listdir(self.path):
    #         if x.endswith(".txt"):
    #             # Prints only text file present in My Folder
    #             files.append(x)
    #     self.files = files


# f1 = Folder('./correct/')
# # rl = f1.readlines()
# # dabid = f1.check_dab_id(rl)
# f1.get_list_files()
# f1.get_list_files()

