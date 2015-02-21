#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import urllib2  
import urllib  
import re  
import threading  
import time  
from Queue import Queue

name=re.compile("nickname\":\"(.+?)\",\"short_nickname")
sex=re.compile("sex\":\"(.+?)\",\"avatar\":")
age=re.compile("\"age\":(.+?),\"he")
height=re.compile("\"height\":(.+?),")
marriage=re.compile("income_link\":\"0\",\"marriage\":(.+?),")
education=re.compile("education\":\"(.+?)\",")
income=re.compile("income\":\"(.+?)\",")
work=re.compile("work_location\":\"(.+?)\",")
#home=re.compile("home_location\":\"(.+?)\",")

queue = Queue()

target = r"http://search.jiayuan.com/?t=10&m=1"
class crawl(threading.Thread):
	def __init__(self,low, high):
		threading.Thread.__init__(self)
		self.low = low
		self.high = high

	def run(self):
            global target
	    global queue
	    print self.low, self.high
            for i in range(self.low, self.high):
		print "bbbbbbbbbbb"
                postdata = urllib.urlencode({
            	    'sex':'f',
            	    'min_age':'19',
            	    'max_age':'26',
            	    'work_location':'51',
            	    'work_sublocation':'5101',
            	    'min_height':'155',
            	    'max_height':'170',
            	    'education':'0',
            	    'edu_more_than':'on',
            	    'house':'0',
            	    'income':'0',
            	    'marriage':'0',
            	    'auto':'0',
            	    'industry':'0',
            	    'children':'0',
            	    'company':'0',
           	    'home_location':'0',
            	    'home_sublocation':'0',
       		    'bloodtype':'0',
            	    'love_location':'0',
            	    'love_sublocation':'0',
            	    'animal':'',
           	    'nation':'0',
           	    'astro':'0',
            	    'belief':'0',
            	    'level':'0',
            	    'ques_love':'0',
            	    'tag':'0',
            	    'online':'0',
            	    'p':str(i)
            	    })
		
            	req = urllib2.Request(
                    url = target,
                    data = postdata
                    )
            	result = urllib2.urlopen(req).read()
	  	queue.put(result)
		#f = open('bb.txt', 'w')
		#f.write(result)
		#f.close()

class tackle(threading.Thread):
	def __init__(self):
                threading.Thread.__init__(self)
		
	def run(self):
		f = open('poem.txt', 'w') # open for 'w'riting  
		global queue
		#print "aaaaaaaa"
		while True:
			while not queue.empty():
				result = queue.get()
                		aa= sex.findall(result)
                		bb= age.findall(result)
                		cc= height.findall(result)
                		dd= marriage.findall(result)
                		ee= education.findall(result)
				ff= name.findall(result)	
				gg= income.findall(result)
				hh= work.findall(result)
				#ii= home.findall(result)
	
                		for string in zip(ff,aa,bb,cc,dd,ee,gg,hh):
    					str1 = string[0].decode('unicode-escape') 
					str2 = string[1].decode('unicode-escape')
					str3 = string[2].decode('unicode-escape')
					str4 = string[3].decode('unicode-escape')
					str5 = string[4].decode('unicode-escape')
					str6 = string[5].decode('unicode-escape')
					str7 = string[6].decode('unicode-escape')
					str8 = string[7].decode('unicode-escape')
					#str9 = string[8].decode('unicode-escape')
					strtemp = "%s, %s, %s, %s, %s, %s, %s,%s\n" %(str1, str2, str3, str4, str5,str6, str7, str8)
					#print str1, str2, str3, str4, str5,str6, str7, str8
					f.write(strtemp)

		 	#print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"		
			time.sleep(6)
            		if queue.empty():
				f.close()
                		break

def main():
	cr1 = crawl(1,250)
	cr2 = crawl(250,500)
	cr3 = crawl(501,750)
	cr4 = crawl(750,1000)
	cr5 = crawl(1000,1250)
	cr6 = crawl(1250,1500)
	cr7 = crawl(1500,1750)
	cr8 = crawl(1750,2000)
	cr9 = crawl(2000,2250)
	cr10 = crawl(2250,2500)


	ta = tackle()


	cr1.start()
	cr2.start()
	cr3.start()
	cr4.start()
    	cr5.start()
	cr6.start()
    	cr7.start()
    	cr8.start()
    	cr9.start()
    	cr10.start()
	

	ta.start()


	cr1.join()
	cr2.join()
	cr3.join()
	cr4.join()
	cr5.join()
    	cr6.join()
    	cr7.join()
    	cr8.join()
    	cr9.join()
    	cr10.join()
	

	ta.join()
if __name__ == '__main__':
	main() 
