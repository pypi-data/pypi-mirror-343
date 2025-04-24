const wrapper = require('./TransmitterWrapper')

class Transmitter {
    static sendCommand(messageArray) {
        return wrapper.sendCommand(messageArray)
    }

    static activate = function (licenseKey) {
        return wrapper.activate(licenseKey)
    }

    static setConfigSource(configSource) {
        return wrapper.setConfigSource(configSource)
    }

    static setJavonetWorkingDirectory(workingDirectory) {
        return wrapper.setJavonetWorkingDirectory(workingDirectory)
    }
}

module.exports = Transmitter
