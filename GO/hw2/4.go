// В генеалогическом древе у каждого человека, кроме родоначальника,
//есть ровно один родитель. Каждом элементу дерева сопоставляется целое
//неотрицательное число, называемое высотой. У родоначальника высота равна 0,
//у любого другого элемента высота на 1 больше, чем у его родителя. Вам дано
//генеалогическое древо, определите высоту всех его элементов.

package main

//import (
//	"fmt"
//	"sort"
//)
//
//func main() {
//	var N int
//	fmt.Scan(&N)
//	// all pairs child: parent
//	tree := make(map[string]string)
//	// dict to count parents
//	persons := make(map[string]int, N)
//
//	for i := 1; i < N; i++ {
//		var child, parent string
//		fmt.Scan(&child, &parent)
//		tree[child] = parent
//		persons[child] = 0
//		persons[parent] = 0
//	}
//	// create slice of each person
//	sliceOfKeys := []string{}
//	// add each person to slice
//	for key, _ := range persons {
//		sliceOfKeys = append(sliceOfKeys, key)
//	}
//	// coount parents
//	for key, _ := range tree {
//		it := key
//		for checkPresence(it, sliceOfKeys) {
//			it = tree[it]
//			persons[key] += 1
//		}
//	}
//	// sort keys
//	sort.Strings(sliceOfKeys)
//	// output each key and value from persons sorted by key
//	for _, key := range sliceOfKeys {
//		if persons[key] > 1 {
//			fmt.Println(key, persons[key]-1)
//		} else {
//			fmt.Println(key, persons[key])
//		}
//	}
//}
//
//func checkPresence(value string, keys []string) bool {
//	for _, v := range keys {
//		if v == value {
//			return true
//		}
//	}
//	return false
//}
