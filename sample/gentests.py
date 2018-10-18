import auger
import main, animal, pet
import foo

with auger.magic([animal, pet, foo.Foo]):
    main.main()
    foo.main()