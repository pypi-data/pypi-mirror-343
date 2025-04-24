const RuntimeName = require('./RuntimeName')

class RuntimeNameHandler {
    /**
     * @param {number} runtimeName
     * @returns {string}
     */
    static getName(runtimeName) {
        switch (runtimeName) {
            case RuntimeName.Clr:
                return 'clr'
            case RuntimeName.Go:
                return 'go'
            case RuntimeName.Jvm:
                return 'jvm'
            case RuntimeName.Netcore:
                return 'netcore'
            case RuntimeName.Perl:
                return 'perl'
            case RuntimeName.Python:
                return 'python'
            case RuntimeName.Ruby:
                return 'ruby'
            case RuntimeName.Nodejs:
                return 'nodejs'
            case RuntimeName.Cpp:
                return 'cpp'
            case RuntimeName.Php:
                return 'php'
            case RuntimeName.Python27:
                return 'python27'
            default:
                throw new Error('Invalid runtime name.')
        }
    }
}

module.exports = RuntimeNameHandler
