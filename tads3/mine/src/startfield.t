#charset "us-ascii"
#include <adv3.h>
#include <en_us.h>
FieldS: OutdoorRoom 'Field, South'
	"I was standing at the south end of a large field. "
	north = FieldCenter
;

FieldCenter: OutdoorRoom 'Field, Center'
	"I was standing in the very center of a large field. "
	south = FieldS
;

+ Pillar: Immovable 'Pillar' 'Pillar'
	"asdf"
;
