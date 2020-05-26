import os
import sys
import cProfile

class DicomFile:

    def __init__(self, filename, parent):
        self._filename = filename
        self._parent = parent

    def getFullPath(self):
        return os.path.join(self._parent.getSeriesDir(), self._filename)

    def __sizeof__(self):
        return sys.getsizeof(self._filename) + 8 # size of reference to parent


class Series:

    def __init__(self, seriesdir, parent):
        self._seriesdir = seriesdir
        self._dicomfiles = []
        self._parent = parent

        if not os.path.isdir(self.getSeriesDir()):
            raise FileNotFoundError("series {} not found".format(
                self.getSeriesDir()))

    def getDicomFiles(self):
        # populate dicomfiles
        if not self._dicomfiles:
            for dcmf in os.listdir(self.getSeriesDir()):
                self._dicomfiles.append(DicomFile(dcmf, self))
        return self._dicomfiles.copy()

    def getSeriesDir(self):
        return os.path.join(self._parent.getStudyDir(), self._seriesdir)

    def __sizeof__(self):
        size = sys.getsizeof(self._seriesdir) + 8
        for f in self._dicomfiles:
            size += sys.getsizeof(f)
        return size

class Study:

    def __init__(self, studydir, parent):
        self._studydir = studydir
        self._series = []
        self._parent = parent

        if not self.getStudyDir():
            raise FileNotFoundError("study {} not found".format(
                self.getStudyDir()))

    def getSeries(self):
        if not self._series:
            # populate series
            for se in os.listdir(self.getStudyDir()):
                self._series.append(Series(se, self))
        return self._series.copy()

    def getStudyDir(self):
        return os.path.join(self._parent.getTopLevelDir(), self._studydir)

    def __sizeof__(self):
        size = sys.getsizeof(self._studydir) + 8
        for s in self._series:
            size += sys.getsizeof(s)
        return size

class DataManager:

    def __init__(self, topleveldir, options = {}):
        self._topleveldir = topleveldir
        self._studies = []

        # check topleveldir exists
        if not os.path.isdir(topleveldir):
            raise FileNotFoundError("top level directory {} not found".
                format(topleveldir))

    def getStudies(self):
        if not self._studies:
            # populate studies
            for st in os.listdir(self._topleveldir):
                self._studies.append(Study(st, self))
        return self._studies.copy()

    def getTopLevelDir(self):
        return self._topleveldir

    def __sizeof__(self):
        size = sys.getsizeof(self._topleveldir)
        for st in self._studies:
            size += sys.getsizeof(st)
        return size


def main():
    dm = DataManager("E:\\oto_test_2018_out")
    studies = dm.getStudies()
    for st in studies:
        series = st.getSeries()
        for se in series:
            dicomfiles = se.getDicomFiles()

if __name__ == '__main__':
    cProfile.run('main()')
    #cProfile.run('walk()')