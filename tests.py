#test wordToNumConverter
import calculator
test_correct = 1

test_word = [6,'billion',342,'million',967,'thousand',42]
if calculator.word_to_num(test_word) != 6342967042:
    test_correct = 0
    print(calculator.word_to_num(test_word))
    print "Failed Converter Test 1"

test_word = ['negative',6,'billion',342,'million',967,'thousand',42]
if calculator.word_to_num(test_word) != -6342967042:
    print(calculator.word_to_num(test_word))
    test_correct = 0
    print "Failed Converter Test 2"

test_word = [6,'zillion',342,'million',967,'thousand',42]
if calculator.word_to_num(test_word) != 'invalidNumber':
    print(calculator.word_to_num(test_word))
    test_correct = 0
    print "Failed Converter Test 3"

test_word = [6,6]
if calculator.word_to_num(test_word) != 'invalidNumber':
    print(calculator.word_to_num(test_word))
    test_correct = 0
    print "Failed Converter Test 4"

test_word = [6]
if calculator.word_to_num(test_word) != 6:
    print(calculator.word_to_num(test_word))
    test_correct = 0
    print "Failed Converter Test 5"

if test_correct ==1:
    print "All  word to number tests passed"
else:
    print "A converter test has failed"

#test calculate
import calculator
test_correct = 1

test_equation = [6,'billion',342,'million',967,'thousand',42,'+',1,'billion','-',5,'million']
test_result = calculator.calculate(test_equation)
true_result = 6342967042 + 1000000000 - 5000000
if abs(test_result - true_result) > abs(true_result*.001):
    print "Calculator Test 1 Failed"
    test_correct = 0

test_equation = [6,'billion',342,'million',967,'thousand',42,'*',1,'billion','-',5,'million']
test_result = calculator.calculate(test_equation)
true_result = 6342967042 * 1000000000 - 5000000
if abs(test_result - true_result) > abs(true_result*.001):
    print "Calculator Test 2 Failed"
    test_correct = 0

test_equation = [1,'million',42,'/',1,'thousand','-',5,'thousand']
test_result = calculator.calculate(test_equation)
true_result = 1000042/1000 - 5000
if abs(test_result - true_result) > abs(true_result*.001):
    print "Calculator Test 3 Failed"
    test_correct = 0

if test_correct ==1:
    print "All  calculator tests passed"
else:
    print "A calculator test has failed"

#test web search
import internet_search
test_list = ['how','i','met','your','mother']
#for i in internet_search.available_browsers:
#    internet_search.websearch(i,test_list)
#internet_search.websearch(None,test_list)

#test computer files search
import computer_search
test_correct = 1

correct_results = ["C:\\Users\\Travis\\Desktop\\personalAssistant\\stars_test_vpa.txt"]
test_results = computer_search.search_computer("stars_test_vpa")
correct_results = set(correct_results)
test_results = set(test_results)
if correct_results != test_results:
    print "Failed Test 1"
    print correct_results
    print test_results
    test_correct = 0
else:
    print "Passed Test 1"

correct_results = ["C:\\Users\\Travis\\Desktop\\DNO\\testfile_for_vpa.txt","C:\\Users\\Travis\\Desktop\\personalAssistant\\testing_vpa\\testfile_for_vpa","E:\\testfile_for_vpa.txt"]
test_results = computer_search.search_computer("testfile_for_vpa")
correct_results = set(correct_results)
test_results = set(test_results)
if correct_results != test_results:
    print "Failed Test 2"
    print correct_results
    print test_results
    test_correct = 0
else:
    print "Passed Test 2"

correct_results = ["C:\\Users\\Travis\\Desktop\\personalAssistant\\testing_vpa"]
test_results = computer_search.search_computer("testing_vpa")
correct_results = set(correct_results)
test_results = set(test_results)
if correct_results != test_results:
    print "Failed Test 3"
    print correct_results
    print test_results
    test_correct = 0
else:
    print "Passed Test 3"

correct_results = ["C:\\Users\\Travis\\Desktop\\personalAssistant\\testing_vpa"]
correct_results = set(correct_results)
test_results = computer_search.search_computer("Testing_VPA")
test_results = set(test_results)
if correct_results != test_results:
    print "Failed Test 4"
    print correct_results
    print test_results
    test_correct = 0
else:
    print "Passed Test 4"

correct_results = ["fileNotFound"]
test_results = computer_search.search_computer("assklajhflksakshalkshddf")
correct_results = set(correct_results)
test_results = set(test_results)
if correct_results != test_results:
    print "Failed Test 5"
    print correct_results
    print test_results
    test_correct = 0
else:
    print "Passed Test 5"

if test_correct != 1:
    print "Computer Search Failed a Test"
else:
    print "All search computer tests passed"

