// Известно, что на доске 8×8 можно расставить 8 ферзей так, чтобы они не били
// друг друга. Вам дана расстановка 8 ферзей на доске, определите, есть ли среди
// них пара бьющих друг друга.

package main

//import (
//	"fmt"
//	"math"
//)
//
//func main() {
//	var a, b [8]float64
//	for i := 0; i < 8; i++ {
//		var aa, bb float64
//		fmt.Scan(&aa, &bb)
//		a[i] = aa
//		b[i] = bb
//	}
//	res := checkProblem(a, b)
//	fmt.Println(res)
//}
//
//func checkProblem(a [8]float64, b [8]float64) string {
//	for i := 0; i < len(a)-1; i++ {
//		for j := i + 1; j < len(a); j++ {
//			if math.Abs(a[i]-a[j]) == math.Abs(b[i]-b[j]) || (a[i] == a[j]) || (b[i] == b[j]) {
//				return "YES"
//
//			}
//		}
//	}
//	return "NO"
//}
