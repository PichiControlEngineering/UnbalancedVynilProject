class notchFilter:
    def __init__(self, f_c, Q, f_s):
        self.f_s = f_s

        omega = 2 * np.pi * f_c / f_s;
        sn = np.sin(omega);
        cs = np.cos(omega);
        alpha = sn / (2 * Q);

        self.a0 = 1 + alpha
        self.a1 = -2 * cs / self.a0
        self.a2 = (1 - alpha) / self.a0
        self.b0 = 1 / self.a0

        self.in1 = 0
        self.in2 = 0

        self.y0 = 0
        self.y1 = 0
        self.y2 = 0
        
    def reset(self):
        self.in1 = 0
        self.in2 = 0

        self.y0 = 0
        self.y1 = 0
        self.y2 = 0

    def increment(self, input):
        self.y0 = self.b0 * (input + self.in2) + self.a1 * (self.in1 - self.y1) - self.a2 * self.y2

        self.in2 = self.in1
        self.in1 = input

        self.y2 = self.y1
        self.y1 = self.y0

        return self.y0
    
    def getFreqResponse(self, N=5000):
        #should really be individual frequencies tested, then compare rms of input and output
        input = np.random.rand(N)
        input -= np.mean(input)
        output = np.zeros(N)

        for i in range(N):
            output[i] = self.increment(input[i])

        fft = abs(np.fft.fft(output))
        freqs = np.fft.fftfreq(N, 1 / self.f_s)

        self.reset()

        return freqs[:N//2], fft[:N//2]
