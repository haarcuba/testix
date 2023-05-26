class TemporaryStorage:
    def create_file(self, filename):
        f = open('/tmp/' + filename, 'w')
        f.write('file_name: ' + filename + '\n\n')
        return f
