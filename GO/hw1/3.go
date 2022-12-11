// N кеглей выставили в один ряд, занумеровав их слева направо числами
//от 1 до N. Затем по этому ряду бросили K шаров, при этом i-й шар
//сбил все кегли с номерами от li до ri включительно. Определите,
//какие кегли остались стоять на месте.

package main

//import (
//	"fmt"
//	"strings"
//)

//func main() {
//	var N, K int
//	fmt.Scan(&N, &K)
//	var bowls string
//	bowls = strings.Repeat("I", N)

//	i := 0
//	for i < K {
//		var lowIdx, highIdx int
//		fmt.Scan(&lowIdx, &highIdx)
//		for idx := lowIdx - 1; idx <= highIdx-1; idx++ {
//			bowls = replaceAtIndex(bowls, '.', idx)
//		}
//		i += 1
//	}

//	fmt.Println(bowls)

//}

//func replaceAtIndex(word string, newValue rune, idx int) string {
//	result := []rune(word)
//	result[idx] = newValue

//	return string(result)
//}

//	func main() {
//		var a, b [8]int32
//
//		i := 0
//		for i < 8 {
//			var aa, bb int32
//			fmt.Scan(&aa, &bb)
//			a[i] = aa
//			b[i] = bb
//
//			i += 1
//		}
//		fmt.Println(a, b)
//	}
