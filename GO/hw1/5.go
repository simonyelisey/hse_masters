// Во входной строке записана последовательность чисел через пробел.
// Для каждого числа выведите слово YES (в отдельной строке), если это
// число ранее встречалось в последовательности или NO, если не встречалось.

package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	text, _ := reader.ReadString('\n')
	var numbers []string
	numbers = strings.Fields(text)

	checkPresence(numbers)

}

func checkPresence(array []string) {
	set := make(map[string]bool)
	for _, key := range array {
		exists := set[key]
		if exists {
			fmt.Println("YES")
		} else {
			set[key] = true
			fmt.Println("NO")
		}
	}
}
