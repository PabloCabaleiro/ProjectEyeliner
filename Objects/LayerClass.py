

class LayerClass(object):

    top_line = None
    _start_line = -1
    _end_line = -1
    bot_line = None

    is_retina = None
    n_capa = -1
    _gaps = None

    def __init__(self, n_capa):
        self.n_capa = n_capa
        self.bot_line = []
        self.top_line = []
        self._start_line = -1
        self._end_line = -1

    def set_top_line(self,top_line, start_point, end_point):
        self._start_line = start_point
        self._end_line = end_point
        for i in range(len(top_line)):
            self.top_line.append((i + self._start_line,top_line[i]))

    def get_pos(self, line, i):
        if line == "top":
            if -1 < i - self._start_line and i < self._end_line:
                return self.top_line[i - self._start_line][1]
            else: return -1
        elif line == "bot":
            if -1 < i - self._start_line and i < self._end_line:
                return self.bot_line[i - self._start_line][1]
            else: return -1

    def interpolate_gaps(self):
        for start, end in self._gaps:
            step = (self.top_line[end - self._start_line][1] - self.top_line[start - self._start_line][1]) / (end - start)
            for k in range(start, end):
                self.top_line[k - self._start_line] = (self.top_line[k - self._start_line][0],round(self.top_line[k - 1 - self._start_line][1] + step))

    def set_bot_line(self, bot_line):
        print(len(bot_line))
        for i in range(len(bot_line)):
            self.bot_line.append((i + self._start_line,bot_line[i]))
        print(len(self.bot_line))

    def set_gaps(self,gaps):
        self._gaps = gaps



