from glob import glob
import os


class File():

    @staticmethod
    def file_names(InputPath):
        '''
        This function acquires dates of sentinel_2 files in the folder
        input:
            InputPath (path for input directory that images are located,
                for example: B:\Khoy\Sentinel2)
        Output:
            1D numeric (double) vector of image dates
        '''
        with open(InputPath) as file_names:
            dates = [i[11:19] for i in file_names if i != '\n']
        return dates

    @staticmethod
    def num_files(InputPath):
        '''
        This function counts number of sentinel2 files in the InputPath
        Input:
            InputPath (path for input directory that images are located,
                for example: B:\Khoy\Sentinel2)
        Output:
            Number of files in InputPath
        '''
        # only reads files beginning with S2 characters (sentinel2 files)
        with open(InputPath) as name_files:
            counts = len(name_files.readlines())
        return counts
