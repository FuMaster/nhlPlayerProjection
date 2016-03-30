import nhlDataParser
from enum import Enum

testAttributes = ['Player','G','A','PTS','GP', 'HIT', 'BLK', 'CF%', 'PIM', 'TK', 'GV']
def getPlayerData():
  playerData, forwardList, defenseList = nhlDataParser.process_players()
  trainingSetF, testingSetF = getForwardSets(forwardList)

  sortedTrainingSetF = getSortedData(trainingSetF)
  sortedTestingSetF = getSortedData(testingSetF)
  return sortedTrainingSetF, sortedTestingSetF
def getSortedData(players):
  pData = []
  tData = []
  for player in players:
    count = 0
    tmpList = []
    for year in player:
      if count > 3:
        break
      if count == 2:
        pData.append(tmpList)
        tmpList = []
      for attr in testAttributes:
        tmpList.append(player[year][attr])

      count += 1
    tData.append(tmpList)

  for p in tData:
    pData.append(p)
  return pData
def getForwardSets(forwardList):
  trainingSetF = []
  testingSetF = []
  count = 0
  for player in forwardList:
    if (count > ((2*len(forwardList))/3)):
      testingSetF.append(player)
    else:
      trainingSetF.append(player)
    count += 1

  return trainingSetF, testingSetF

class DataSet(object):

  def __init__(self, stats, labels, one_hot=False):
    """Construct a DataSet.
    one_hot arg is used only if fake_data is true. 
    """
    assert len(stats) == len(labels), (
          'len(stats): %s len(labels): %s' % (len(stats),len(labels)) )
    self._num_examples = len(stats)

    self._stats = stats
    self._labels = labels
    self._epochs_completed = 0
    self._index_in_epoch = 0

  @property
  def stats(self):
    return self._stats

  @property
  def labels(self):
    return self._labels

  @property
  def num_examples(self):
    return self._num_examples

  @property
  def epochs_completed(self):
    return self._epochs_completed

  def next_batch(self, batch_size):
    """Return the next `batch_size` examples from this data set."""
    start = self._index_in_epoch
    self._index_in_epoch += batch_size
    if self._index_in_epoch > self._num_examples:
      # Finished epoch
      self._epochs_completed += 1
      # Shuffle the data
      perm = numpy.arange(self._num_examples)
      numpy.random.shuffle(perm)
      self._stats = self._stats[perm]
      self._labels = self._labels[perm]
      # Start next epoch
      start = 0
      self._index_in_epoch = batch_size
      assert batch_size <= self._num_examples
    end = self._index_in_epoch
    return self._stats[start:end], self._labels[start:end]


def read_data_sets(one_hot=True):
  class DataSets(object):
    pass
  data_sets = DataSets()
  trainSetF, testSetF = getPlayerData()
  #extract data from forwards in their first 2 seasons
  

  labelSize = len(trainSetF)/2
  
  train_stats = trainSetF[labelSize:]
  train_labels = trainSetF[:labelSize]

  test_stats = testSetF[len(testSetF)/2:]
  test_labels = testSetF[:len(testSetF)/2]

  '''
  print train_stats[0], train_labels[0]
  print train_stats[labelSize-1], train_labels[labelSize-1]

  print test_stats[0], test_labels[0]
  print test_stats[(len(testSetF)/2)-1], test_labels[(len(testSetF)/2)-1]
  '''
  data_sets.train = DataSet(train_stats, train_labels)
  data_sets.test = DataSet(test_stats, test_labels)

  return data_sets

read_data_sets()