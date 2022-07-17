import os, sys, subprocess
import xbmc, xbmcgui, xbmcaddon

__addon__    = sys.modules[ '__main__' ].__addon__
__addonid__  = sys.modules[ '__main__' ].__addonid__
__cwd__      = sys.modules[ '__main__' ].__cwd__
__skindir__  = xbmc.getSkinDir()
__skinhome__ = xbmc.translatePath( os.path.join( 'special://home/addons/', __skindir__, 'addon.xml' ).encode('utf-8') )
__skinxbmc__ = xbmc.translatePath( os.path.join( 'special://xbmc/addons/', __skindir__, 'addon.xml' ).encode('utf-8') )

class Screensaver(xbmcgui.WindowXMLDialog):
    def __init__( self, *args, **kwargs ):
        pass

    def onInit(self):
        self._is_powered = True
        self.Monitor = MyMonitor(action = self._power_on)
        self.toggle_pwr()

    def _power_on(self):
        self.toggle_pwr()
        self.close()

    def toggle_pwr(self):
        if self._is_powered:
            arg = '0'
            xbmc.log(msg="TMDS to 0")
        else:
            arg = '1'
            xbmc.log(msg="TMDS to 1")
        try:
            xbmc.log(msg="Toggling HDMI TMDS clock", level=xbmc.LOGDEBUG)
            f = open("/sys/class/amhdmitx/amhdmitx0/phy", "w")
            f.write(arg)
            f.close()
        except:
            xbmc.log(msg="Can't toggle HDMI TMDS clock", level=xbmc.LOGERROR)
        try:
            xbmc.log(msg="Toggling LED", level=xbmc.LOGDEBUG)
            f = open("/sys/class/leds/led-sys/brightness", "w")
            f.write(arg)
            f.close()
        except:
            xbmc.log(msg="Error toggling LED", level=xbmc.LOGERROR)
        try:
            if self._is_powered:
                start_cmd="stop"
                xbmc.log(msg="ConnMan is to stop")
            else:
                start_cmd="start"
                xbmc.log("ConnMan is to start")
            xbmc.log(msg="Toggling network connectivity", level=xbmc.LOGDEBUG)
            os.system("/bin/systemctl " + start_cmd + " connman")
        except:
            xbmc.log(msg="Can't toggle network connectivity", level=xbmc.LOGERROR)
        try:
            if self._is_powered:
                governor="powersave"
                xbmc.log(msg="Using powersave governor")
            else:
                governor="ondemand"
                xbmc.log(msg="Using ondemand governor")
            xbmc.log(msg="Toggling CPU governor", level=xbmc.LOGDEBUG)
            f = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor", "w")
            f.write(governor)
            f.close()
        except:
            xbmc.log(msg="Can't toggle CPU governor", level=xbmc.LOGERROR)
        self._is_powered = not self._is_powered

class MyMonitor(xbmc.Monitor):
    def __init__( self, *args, **kwargs ):
        self.action = kwargs['action']

    def onScreensaverDeactivated(self):
        self.action()
