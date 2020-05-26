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
        self._dicomfiles = None
        self._parent = parent

        if not os.path.isdir(self.getSeriesDir()):
            raise FileNotFoundError("series {} not found".format(
                self.getSeriesDir()))

    def getDicomFiles(self):
        # populate dicomfiles
        if not self._dicomfiles:
            dicomfiles = []
            for dcmf in os.listdir(self.getSeriesDir()):
                dicomfiles.append(DicomFile(dcmf, self))
            self._dicomfiles = tuple(dicomfiles)
        return self._dicomfiles

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
        self._series = None
        self._parent = parent

        if not self.getStudyDir():
            raise FileNotFoundError("study {} not found".format(
                self.getStudyDir()))

    def getSeries(self):
        if not self._series:
            # populate series
            series = []
            for se in os.listdir(self.getStudyDir()):
                series.append(Series(se, self))
            self._series = tuple(series)
        return self._series

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
        self._studies = None

        # check topleveldir exists
        if not os.path.isdir(topleveldir):
            raise FileNotFoundError("top level directory {} not found".
                format(topleveldir))

    def getStudies(self):
        if not self._studies:
            # populate studies
            studies = []
            for st in os.listdir(self._topleveldir):
                studies.append(Study(st, self))
            self._studies = tuple(studies)
        return self._studies

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
    for st in studies[0:5]:
        series = st.getSeries()
        for se in series[0:5]:
            dicomfiles = se.getDicomFiles()

if __name__ == '__main__':
    cProfile.run('main()')
    #cProfile.run('walk()')