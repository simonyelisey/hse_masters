// пополнение
// снятие
// запрос остатка
// перевод между счетами
// начисление процентов всем клиентам

package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

type Account struct {
	Name    string
	Balance float64
}

type Transfer struct {
	from   string
	to     string
	amount float64
}

type Accounts map[string]Account

func (a Accounts) CreateClient(c Account) {
	a[c.Name] = c
}

func (a Accounts) ReturnClient(name string) Account {
	return a[name]
}

func (a Accounts) UpdateClient(c Account) {
	a[c.Name] = c
}

func (a *Account) Deposit(amount float64) {
	a.Balance += amount
}

func (a *Account) Withdraw(amount float64) {
	a.Balance -= amount
}

func (a *Account) ShowBalance() float64 {
	return a.Balance
}

func (a Accounts) TransferMoney(t Transfer) {
	sender := a.ReturnClient(t.from)
	reciever := a.ReturnClient(t.to)
	//if sender.Balance < t.amount {
	//	return fmt.Errorf("there is no enough money")
	//}
	sender.Withdraw(t.amount)
	reciever.Deposit(t.amount)

	a.UpdateClient(sender)
	a.UpdateClient(reciever)

	//return nil
}

func (a Accounts) Income(p float64) {
	for k := range a {
		client := a.ReturnClient(k)
		if client.Balance > 0 {
			income, _ := math.Modf(client.Balance * (p / 100))
			client.Deposit(income)
			a.UpdateClient(client)
		}
	}
}

func (a Accounts) CheckPresence(name string) bool {
	if a[name].Name == "" {
		return false
	}
	return true
}

func main() {
	acc := Accounts{}
	scanner := bufio.NewScanner(os.Stdin)
	var all_lines []string
	for {
		scanner.Scan()
		l := scanner.Text()
		// break the loop if line is empty
		if len(l) == 0 {
			break
		}
		all_lines = append(all_lines, strings.TrimSpace(l))
	}
	for _, l := range all_lines {
		command := strings.Split(l, " ")
		if command[0] == "DEPOSIT" {
			name := command[1]
			amount, _ := strconv.ParseFloat(command[2], 64)
			if acc.CheckPresence(name) {
				client := acc[name]
				client.Deposit(amount)
				acc.UpdateClient(client)
			} else {
				client := Account{
					Name:    name,
					Balance: amount,
				}
				acc.CreateClient(client)
			}
		} else if command[0] == "WITHDRAW" {
			name := command[1]
			amount, _ := strconv.ParseFloat(command[2], 64)
			if acc.CheckPresence(name) {
				client := acc.ReturnClient(name)
				client.Withdraw(amount)
				acc.UpdateClient(client)
			} else {
				client := Account{
					Name:    name,
					Balance: -amount, // may be 0 here
				}
				acc.CreateClient(client)
			}
		} else if command[0] == "BALANCE" {
			name := command[1]
			if acc.CheckPresence(name) {
				client := acc[name]
				balance := client.ShowBalance()
				fmt.Println(int(balance))
			} else {
				fmt.Println("ERROR")
			}
		} else if command[0] == "TRANSFER" {
			names := []string{command[1], command[2]}
			amount, _ := strconv.ParseFloat(command[3], 64)
			transfer := Transfer{
				from:   names[0],
				to:     names[1],
				amount: amount,
			}
			for _, name := range names {
				if !acc.CheckPresence(name) {
					client := Account{
						Name:    name,
						Balance: 0,
					}
					acc.CreateClient(client)
				}
			}
			acc.TransferMoney(transfer)
		} else {
			income, _ := strconv.ParseFloat(command[1], 64)
			acc.Income(income)
		}
	}
}
