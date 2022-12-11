// B. Минимальный делитель числа
// Дано натуральное число n>1. Выведите его наименьший делитель, отличный от 1
package main

import (
	"fmt"
	"math"
)

func main() {
	var number int
	fmt.Scan(&number)
	returnNumber := minDivision(number)

	fmt.Println(returnNumber)

}

func minDivision(number int) int {
	for i := 2; i < int(math.Sqrt(float64(number)))+1; i++ {
		rest := number % i
		if rest == 0 {
			return i
		}
	}
	return number
}
