const AbstractHandler = require('./AbstractHandler')
const LoadLibraryHandler = require('./LoadLibraryHandler')
const NamespaceCache = require('../namespaceCache/NamespaceCache')
const TypeCache = require('../typeCache/TypeCache')

class GetTypeHandler extends AbstractHandler {
    constructor() {
        super()
        this.requiredParametersCount = 1
        this.namespaceCache = new NamespaceCache()
        this.typeCache = new TypeCache()
    }

    process(command) {
        try {
            if (command.payload.length < this.requiredParametersCount) {
                throw new Error('Get Type parameters mismatch')
            }
            const { payload } = command
            let typeName = payload[0]
            typeName = typeName.replace('.js', '')
            let typeToReturn = global[typeName]
            if (typeToReturn === undefined) {
                let message = `Type ${typeName} not found\n`
                message += 'Available types:\n'
                message += this.getAvailableTypes().join('\n')
                throw new Error(message)
            }

            if (
                (this.namespaceCache.isNamespaceCacheEmpty() && this.typeCache.isTypeCacheEmpty()) || // both caches are empty
                this.namespaceCache.isTypeAllowed(typeToReturn) || // namespace is allowed
                this.typeCache.isTypeAllowed(typeToReturn) // type is allowed
            ) {
                // continue - type is allowed
            } else {
                let allowed_namespaces = this.namespaceCache.getCachedNamespaces().join(', ')
                let allowed_types = this.typeCache.getCachedTypes().join(', ')
                throw new Error(
                    `Type ${typeToReturn.name} not allowed. \nAllowed namespaces: ${allowed_namespaces}\nAllowed types: ${allowed_types}`
                )
            }

            return typeToReturn
        } catch (error) {
            throw this.process_stack_trace(error, this.constructor.name)
        }
    }

    getAvailableTypes() {
        let availableTypes = []
        LoadLibraryHandler.getLoadedLibraries().forEach((lib) => {
            const moduleExports = require(lib)
            availableTypes.push(moduleExports.name)
            Object.keys(moduleExports).forEach((key) => {
                availableTypes.push(key)
            })
        })
        return availableTypes
    }
}

module.exports = new GetTypeHandler()
