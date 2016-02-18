from creeper_pp.shell_service import ShellService
from creeper_pp.io_service import IoService

class MrcService(object):
    features_count = 13
    features_indexes = [[0 for x in range(2)] for x in range(features_count)]
    nlet = [0,2] #number of letters */
    nphon = [2,4] #number of phomemes */
    nsyl = [4,5]    # number of syllables in word*/
    kffreq = [5,10] #k & f frequency*/
    kfncats = [10,12] #no of k&f categories */
    kfnsamp = [12,15] #no of k&f samples */
    t_l = [15,21] #Thorndyke-Lorge freq*/
    brownf = [21,25] #Brown's Spoken frequency */
    fam = [25,28] #Familiarity*/
    conc = [28,31] #Concreteness*/
    imag = [31,34] #Imagery*/
    meanc = [34,37] #mean Colerado meaningfulness*/
    meanp = [37,40] #mean pavio meaningfulness*/
    aoa = [40,43] #mean pavio meaningfulness*/
    features_indexes[0][0] = nlet[0]
    features_indexes[0][1] = nlet[1]
    features_indexes[1][0] = nphon[0]
    features_indexes[1][1] = nphon[1]
    features_indexes[2][0] = nsyl[0]
    features_indexes[2][1] = nsyl[1]
    features_indexes[3][0] = kffreq[0]
    features_indexes[3][1] = kffreq[1]
    features_indexes[3][0] = kfncats[0]
    features_indexes[3][1] = kfncats[1]
    features_indexes[4][0] = kfncats[0]
    features_indexes[4][1] = kfncats[1]
    features_indexes[5][0] = t_l[0]
    features_indexes[5][1] = t_l[1]
    features_indexes[6][0] = brownf[0]
    features_indexes[6][1] = brownf[1]
    features_indexes[7][0] = fam[0]
    features_indexes[7][1] = fam[1]
    features_indexes[8][0] = conc[0]
    features_indexes[8][1] = conc[1]
    features_indexes[9][0] = imag[0]
    features_indexes[9][1] = imag[1]
    features_indexes[10][0] = meanc[0]
    features_indexes[10][1] = meanc[1]
    features_indexes[11][0] = meanp[0]
    features_indexes[11][1] = meanp[1]
    features_indexes[12][0] = aoa[0]
    features_indexes[12][1] = aoa[1]

    mrc_command = './getentry input'

    def __init__(self, mrc_location):
        self.mrc_location = mrc_location
        self.input_file = mrc_location + '/input'

    def get_vector(self, words):
        features = [0 for x in range(self.features_count)]
        for i in range(self.features_count):
            features[i] = 0

        IoService.write_array_to_file(self.input_file, sorted(words))
        mrc_output = ShellService.execute(self.mrc_command, self.mrc_location).split('\n') # removing list empty line
        for line in mrc_output[0:-1]:
            for i in range(self.features_count):
                features[i] += int(line[self.features_indexes[i][0] : self.features_indexes[i][1]])
        for i in range(self.features_count):
            features[i] /= len(mrc_output)
        return features
