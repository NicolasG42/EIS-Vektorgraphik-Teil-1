abstract class Datum(val tag: Int, val monat: Int, val jahr: Int) {
  def print_date(): String
  def print_date_short(): String
}

class DatumDE(tag: Int, monat: Int, jahr: Int) extends Datum(tag, monat, jahr) {
  def print_date(): String = {
    val monate = Array("Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember")
    s"$tag. ${monate(monat - 1)} $jahr"
  }

  def print_date_short(): String = {
    f"$tag%02d.$monat%02d.${jahr % 100}%02d"
  }
}

class DatumUS(tag: Int, monat: Int, jahr: Int) extends Datum(tag, monat, jahr) {
  def print_date(): String = {
    val monate = Array("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
    s"${monate(monat - 1)} $tag $jahr"
  }

  def print_date_short(): String = {
    f"$monat%02d/$tag%02d/${jahr % 100}%02d"
  }
}

object DatumTest {
  def main(args: Array[String]): Unit = {
    val datumDE = new DatumDE(24, 12, 2024)
    val datumUS = new DatumUS(24, 12, 2024)

    println("Deutsch ausfuehrlich: " + datumDE.print_date())
    println("Deutsch kurz: " + datumDE.print_date_short())
    println("US ausfuehrlich: " + datumUS.print_date())
    println("US kurz: " + datumUS.print_date_short())
  }
}
