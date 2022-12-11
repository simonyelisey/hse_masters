// Формат ввода
//Каждая строка входного файла содержит фамилию кандидата, за которого отдают голоса
//выборщики этого штата, затем через пробел идет количество выборщиков, отдавших голоса за этого кандидата.
//
//Формат вывода
//Выведите фамилии всех кандидатов в лексикографическом порядке, затем, через пробел,
//количество отданных за них голосов.

package main

//import (
//	"bufio"
//	"fmt"
//	"log"
//	"os"
//	"sort"
//	"strconv"
//	"strings"
//)
//
//func main() {
//	scanner := bufio.NewScanner(os.Stdin)
//	var all_lines []string
//	for {
//		scanner.Scan()
//		l := scanner.Text()
//		// break the loop if line is empty
//		if len(l) == 0 {
//			break
//		}
//		//l = strings.Trim(l)
//		all_lines = append(all_lines, strings.TrimSpace(l))
//	}
//	err := scanner.Err()
//	if err != nil {
//		log.Fatal(err)
//	}
//
//	countVotes := make(map[string]int)
//	for _, value := range all_lines {
//		pair := strings.Split(value, " ")
//		votes, _ := strconv.Atoi(pair[1])
//		countVotes[pair[0]] += votes
//	}
//	keys := []string{}
//	for key, _ := range countVotes {
//		keys = append(keys, key)
//	}
//	sort.Strings(keys)
//	for _, key := range keys {
//		fmt.Println(key, countVotes[key])
//	}
//}
