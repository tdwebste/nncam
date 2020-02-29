import nncam

class App:
    def __init__(self):
        self.hcam = None
        self.buffer = None
        self.total = 0

# the vast majority of callbacks come from nncam.dll/so/dylib internal threads
    @staticmethod
    def cameraCallback(nEvent, ctx):
        if nEvent == nncam.NNCAM_EVENT_IMAGE:
            ctx.CameraCallback(nEvent)

    def CameraCallback(self, nEvent):
        if nEvent == nncam.NNCAM_EVENT_IMAGE:
            try:
                self.hcam.PullImageV2(self.buffer, 24, None)
                self.total += 1
                print('pull image ok, total = {}'.format(self.total))
            except nncam.HRESULTException:
                print('pull image failed')
        else:
            print('event callback: {}'.format(nEvent))

    def run(self):
        a = nncam.NnCam.EnumV2()
        if len(a) > 0:
            print('{}: flag = {:#x}, preview = {}, still = {}'.format(a[0].displayname, a[0].model.flag, a[0].model.preview, a[0].model.still))
            for r in a[0].model.res:
                print('\t = [{} x {}]'.format(r.width, r.height))
            self.hcam = nncam.NnCam.Open(a[0].id)
            if self.hcam:
                try:
                    width, height = self.hcam.get_Size()
                    bufsize = ((width * 24 + 31) // 32 * 4) * height
                    print('image size: {} x {}, bufsize = {}'.format(width, height, bufsize))
                    self.buffer = bytes(bufsize)
                    if self.buffer:
                        try:
                            self.hcam.StartPullModeWithCallback(self.cameraCallback, self)
                        except nncam.HRESULTException:
                            print('failed to start camera')
                    input('press ENTER to exit')
                finally:
                    self.hcam.Close()
                    self.hcam = None
                    self.buffer = None
            else:
                print('failed to open camera')
        else:
            print('no camera found')

if __name__ == '__main__':
    app = App()
    app.run()