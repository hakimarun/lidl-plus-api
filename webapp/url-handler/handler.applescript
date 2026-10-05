-- Faengt Aufrufe von com.lidlplus.app ab und gibt die Adresse an den lokalen
-- Lidl Plus API Explorer weiter, der daraus das Token holt.
on open location this_URL
	try
		set theResult to do shell script "curl -s -X POST http://127.0.0.1:8777/api/auth/catch --data-urlencode " & quoted form of ("url=" & this_URL)
		display notification theResult with title "Lidl Plus"
	on error errMsg
		display notification errMsg with title "Lidl Plus Fehler"
	end try
end open location

-- Falls per Doppelklick gestartet, nur ein Hinweis.
on run
	display notification "Bereit. Starte den Login im API Explorer." with title "Lidl Plus"
end run
