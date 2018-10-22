import auger
import main, animal, pet
import foo
import properties

with auger.magic([animal, pet, foo.Foo]):
    main.main()
    foo.main()
    properties.main()