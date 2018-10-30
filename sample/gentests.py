import auger
import main, animal, pet
import foo
import properties
import functions

with auger.magic([animal, pet, foo.Foo, properties.Language, functions]):
    main.main()
    foo.main()
    properties.main()
    functions.main()
