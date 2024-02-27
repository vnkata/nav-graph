build_and_run: build run

clean: 
	@rm -vrf mypackage
	@rm -vrf Log

build:
	@mkdir Log
	@groovyc Code/Identifier.groovy
	@groovyc Code/State.groovy
	@groovyc Code/GetText.groovy	
	@groovyc Code/template.groovy
	@echo 'Build completed'

build_file:
	@groovyc $(FILE)

run: 

	@groovy -cp . build.groovy > Log/log.txt
	@python Python/CheckLog.py 