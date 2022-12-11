// теорема Лагранжа

package main

import (
	"fmt"
	"strconv"
	"strings"
)

func main() {
	var number int
	fmt.Scan(&number)
	squares := []string{}
	for i := 0; i*i <= number; i++ {
		for j := i; j*j <= number; j++ {
			for k := j; k*k <= number; k++ {
				for l := k; l*l <= number; l++ {
					if i*i+j*j+k*k+l*l == number {
						s := []string{strconv.Itoa(l), strconv.Itoa(k), strconv.Itoa(j), strconv.Itoa(i)}
						ss := []string{}
						for _, v := range s {
							if v != "0" {
								ss = append(ss, v)
							}
						}
						squares = append(squares, strings.Join(ss, " "))
					}
				}
			}
		}
	}
	fmt.Println(squares[0])
}
