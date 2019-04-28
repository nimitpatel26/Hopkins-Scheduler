

function postData(input) {
  $.ajax({
    type: "POST",
    url: "/reverse_pca.py"
  });
}


class PersonType{
  constructor (personTypeName, shift, hoursRequired, location, constraints){
    this.personTypeName = personTypeName;
    this.shift = shift;
    this.hoursRequired = hoursRequired;
    this.location = location;
  }
}


class Shift{
  constructor(numberOfShifts, length) {
    this.numberOfShifts = numberOfShifts;
    this.length = length;
  }

}


class Person{
  constructor(name, personType, hoursCompleted, constraints) {
    this.name = name;
    this.personType = personType;
    this.hoursCompleted = hoursCompleted;
  }


}


// Constraints would also include the priority
class Constraints{
  constructor(inclusion, exclusion) {
    this.inclusion = inclusion;
    this.exclusion = exclusion;
  }

}



var DoctorShift = [new Shift(15, 8), new Shift(4, 12)];
var Doctor = new PersonType("Doctor", DoctorShift, 122, "Main_Hospital");

var doc1 = new Person("James", Doctor, 100);
var doc2 = new Person("Melissa", Doctor, 77);
var doc3 = new Person("Alex", Doctor, 25);
var doc4 = new Person("Ryan", Doctor, 30);
var doc5 = new Person("Cynthia", Doctor, 45);


var NurseShift = [new Shift(21, 8)];
var NurseConstraint = new Constraints([0, 5, 8, 11, 14]);
var Nurse = new PersonType("Nurse", NurseShift, 200, "Nursery", NurseConstraint);

var nur1 = new Person("Chris", Nurse, 78);
var nur2Constraints = new Constraints([0, 1, 2])
var nur2 = new Person("Josh", Nurse, 100, nur2Constraints);
var nur3 = new Person("Ashley", Nurse, 55);
var nur4 = new Person("Brianna", Nurse, 121);
var nur5 = new Person("Madison", Nurse, 95);


