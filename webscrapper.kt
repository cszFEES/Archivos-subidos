package com.example.lamprechtvids

import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import kotlinx.coroutines.*
import org.jsoup.Jsoup

class MainActivity : AppCompatActivity() {
    private lateinit var btnScrape: Button
    private lateinit var tvResults: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        btnScrape = findViewById(R.id.btnScrape)
        tvResults = findViewById(R.id.tvResults)

        btnScrape.setOnClickListener {
            CoroutineScope(Dispatchers.IO).launch {
                val result = scrapeVideos()
                withContext(Dispatchers.Main) {
                    tvResults.text = result
                }
            }
        }
    }

    private fun scrapeVideos(): String {
        val url = "https://historyreviewed.best/"
        val builder = StringBuilder()

        return try {
            val doc = Jsoup.connect(url).get()
            val links = doc.select("div.article-content a")

            for (link in links) {
                val text = link.text()
                if (text.startsWith("Video:")) {
                    val href = link.absUrl("href")
                    val title = link.attr("title")
                    builder.append("• $title\n$href\n\n")
                }
            }

            if (builder.isEmpty()) "No video links found."
            else builder.toString()

        } catch (e: Exception) {
            "Error: ${e.message}"
        }
    }
}
