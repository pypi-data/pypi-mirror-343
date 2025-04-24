const AbstractHandler = require('./AbstractHandler')

class CastingHandler extends AbstractHandler {
    // eslint-disable-next-line no-unused-vars
    process(command) {
        throw new Error(`Dynamically typed languages are not supporting casting`)
    }
}

module.exports = new CastingHandler()
