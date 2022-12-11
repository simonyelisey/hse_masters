// Дан текст. Выведите слово, которое в этом тексте встречается чаще всего.
// Если таких слов несколько, выведите то, которое меньше в лексикографическом порядке.

package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	var all_lines []string
	for {
		scanner.Scan()
		l := scanner.Text()
		// break the loop if line is empty
		if len(l) == 0 {
			break
		}
		//l = strings.Trim(l)
		all_lines = append(all_lines, strings.TrimSpace(l))
	}
	err := scanner.Err()
	if err != nil {
		log.Fatal(err)
	}

	arr := strings.Split(strings.Join(all_lines, " "), " ")

	wordCount := countWords(arr)
	mapValues := []int{}
	for _, v := range wordCount {
		mapValues = append(mapValues, v)
	}
	maxValue := 0
	for _, v := range mapValues {
		if v > maxValue {
			maxValue = v
		}
	}
	maxValueKeys := []string{}
	for k, v := range wordCount {
		if v == maxValue {
			maxValueKeys = append(maxValueKeys, k)
		}
	}
	minKey := maxValueKeys[0]
	for _, v := range maxValueKeys[1:] {
		if v < minKey {
			minKey = v
		}
	}
	fmt.Println(minKey)
}

func countWords(array []string) map[string]int {
	counter := make(map[string]int)
	for _, value := range array {
		counter[value] += 1
	}
	return counter
}
