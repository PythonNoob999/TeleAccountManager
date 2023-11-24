
##### to control multiple accounts using this tool, `after running it ofcourse`

##### You will use a format that looks like this
```
/command_name
arg1=value
arg2=value
```

### Default arguments

#### there are some arguments that is Default on a specific value

1. count
##### this tells how much account are you using for this task!
##### count can be:
`max`
> To use all your accounts

`some_number`
> How much accounts are you going to use, the start point by default is 0

`start_number-stop_number`
> Which accounts are you going to use based on the start index and end index, Example:
> 10-25
> this will go from the account number 10 in your Tool, to account number 25

1. max_perf
##### Used to indicate whether to use the fastest way to do all the tasks or not, False by default

> INFO: if max_perf = True
> then every `task` the account has to do will be collected as Coroutines or Asyncio tasks, then done all in the same time using `asyncio.gather()`