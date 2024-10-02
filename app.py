from flask import Flask, request, render_template, jsonify
import google.generativeai as genai
import json
import os
import base64

app = Flask(__name__)

# Set your Google API Key
GOOGLE_API_KEY = 'AIzaSyC5fWuMrY1ZqQZKe17DkwGVu_vi172s7J8'  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)
model = 'gemini-1.5-flash' 
gemini = genai.GenerativeModel(model_name=model)
CHAT_HISTORY_FILE = 'chat_history.json'

@app.route('/')
def index():
    # Load existing chat history
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, 'r') as f:
            chat_history = json.load(f)
    else:
        chat_history = []
    
    return render_template('index.html', chat_history=chat_history)

@app.route('/generate', methods=['POST'])
def generate():
    user_input = request.form['user_input']
    print(user_input)
    # Prepare the request data as in your original notebook
    model = 'gemini-1.5-flash' # @param {isTemplate: true}
    contents_b64 = 'W3sicGFydHMiOlt7InRleHQiOiJpbnB1dDogSGksIEknbSByZWFsbHkgYW54aW91cyBhYm91dCBteSB1cGNvbWluZyBleGFtcy4gSSBmZWVsIGxpa2UgSSBjYW4ndCBjb25jZW50cmF0ZSBhbmQgaXQncyBvdmVyd2hlbG1pbmcuIn0seyJ0ZXh0Ijoib3V0cHV0OiBJJ20gcmVhbGx5IHNvcnJ5IHlvdSdyZSBmZWVsaW5nIHRoaXMgd2F5IHJpZ2h0IG5vdy4gRXhhbSBzdHJlc3MgY2FuIGJlIHRvdWdoLCBidXQgaXQncyBpbXBvcnRhbnQgdG8gdGFrZSB0aGluZ3Mgb25lIHN0ZXAgYXQgYSB0aW1lLiBIYXZlIHlvdSB0cmllZCBhbnkgcmVsYXhhdGlvbiB0ZWNobmlxdWVzLCBsaWtlIGRlZXAgYnJlYXRoaW5nIG9yIGEgc2hvcnQgYnJlYWsgdG8gY2xlYXIgeW91ciBtaW5kPyBJdCdzIGFsc28gaGVscGZ1bCB0byBjcmVhdGUgYSBzbWFsbCBzdHVkeSBzY2hlZHVsZSBzbyB0aGF0IHlvdSBjYW4gZm9jdXMgb24gb25lIHRhc2sgYXQgYSB0aW1lLiBIb3cgYXJlIHlvdSBmZWVsaW5nIGFib3V0IHlvdXIgc3R1ZHkgcHJvZ3Jlc3Mgc28gZmFyPyJ9LHsidGV4dCI6ImlucHV0OiBJJ3ZlIGJlZW4gZmVlbGluZyByZWFsbHkgbG9uZWx5IGF0IGNvbGxlZ2UuIEkgZG9u4oCZdCBrbm93IGhvdyB0byBtYWtlIG5ldyBmcmllbmRzLCBhbmQgaXTigJlzIHN0YXJ0aW5nIHRvIGFmZmVjdCBtZS4ifSx7InRleHQiOiJvdXRwdXQ6IEknbSByZWFsbHkgc29ycnkgeW91J3JlIGZlZWxpbmcgbG9uZWx5LiBDb2xsZWdlIGNhbiBmZWVsIGlzb2xhdGluZywgZXNwZWNpYWxseSBpZiBpdCdzIGhhcmQgdG8gY29ubmVjdCB3aXRoIG90aGVycyBhdCBmaXJzdC4gU29tZXRpbWVzIGpvaW5pbmcgYSBjbHViIG9yIHN0dWR5IGdyb3VwIGNhbiBiZSBhIGdvb2Qgd2F5IHRvIG1lZXQgcGVvcGxlIHdobyBzaGFyZSBzaW1pbGFyIGludGVyZXN0cy4gSXQgY2FuIGFsc28gaGVscCB0byByZWFjaCBvdXQgdG8gY2xhc3NtYXRlc+KAlHNvbWV0aW1lcywgb3RoZXJzIGZlZWwgdGhlIHNhbWUgd2F5IGJ1dCBhcmVuJ3Qgc3VyZSBob3cgdG8gc3RhcnQgYSBjb252ZXJzYXRpb24uIFdvdWxkIHlvdSBsaWtlIHNvbWUgaWRlYXMgZm9yIGNsdWJzIG9yIGdyb3VwcyB0aGF0IHlvdSBjb3VsZCBleHBsb3JlPyJ9LHsidGV4dCI6ImlucHV0OiBJJ20gZHJvd25pbmcgaW4gYXNzaWdubWVudHMuIEkgZG9uJ3Qga25vdyBob3cgdG8ga2VlcCB1cCwgYW5kIEkgZmVlbCBsaWtlIEknbSBmYWxsaW5nIGJlaGluZC4ifSx7InRleHQiOiJvdXRwdXQ6IEl0IHNvdW5kcyBsaWtlIHlvdSdyZSBjYXJyeWluZyBhIGxvdCByaWdodCBub3csIGFuZCBpdCdzIHVuZGVyc3RhbmRhYmxlIHRvIGZlZWwgb3ZlcndoZWxtZWQuIEJyZWFraW5nIHRhc2tzIGRvd24gaW50byBzbWFsbGVyIHBpZWNlcyBtaWdodCBoZWxw4oCUY2FuIHlvdSBmb2N1cyBvbiBvbmUgYXNzaWdubWVudCBhdCBhIHRpbWU/IEFsc28sIGRvbuKAmXQgaGVzaXRhdGUgdG8gYXNrIHlvdXIgcHJvZmVzc29ycyBvciBwZWVycyBmb3IgY2xhcmlmaWNhdGlvbiBvciBleHRlbnNpb25zIGlmIG5lZWRlZC4gSXTigJlzIG9rYXkgdG8gc2VlayBoZWxwLiBEbyB5b3Ugd2FudCBzb21lIHRpcHMgb24gbWFuYWdpbmcgeW91ciB0aW1lLCBvciBtYXliZSBhIGd1aWRlIHRvIHByaW9yaXRpemUgeW91ciB0YXNrcz8ifSx7InRleHQiOiJpbnB1dDogSSBqdXN0IGZlZWwgc28gZG93biBsYXRlbHksIGFuZCBJIGRvbid0IGhhdmUgdGhlIGVuZXJneSB0byBkbyBhbnl0aGluZyBhbnltb3JlLiBJIGRvbuKAmXQga25vdyB3aGF04oCZcyB3cm9uZyB3aXRoIG1lLiJ9LHsidGV4dCI6Im91dHB1dDogSSdtIHJlYWxseSBzb3JyeSB5b3UncmUgZmVlbGluZyB0aGlzIHdheS4gSXQncyBoYXJkIHdoZW4geW91J3JlIGdvaW5nIHRocm91Z2ggcGVyaW9kcyBvZiBsb3cgZW5lcmd5IGFuZCBzYWRuZXNzLiBJdCBtaWdodCBiZSBoZWxwZnVsIHRvIHJlYWNoIG91dCB0byBzb21lb25lIHlvdSB0cnVzdCwgbGlrZSBhIGZyaWVuZCBvciBjb3Vuc2Vsb3IsIHRvIHRhbGsgYWJvdXQgd2hhdCB5b3UncmUgZXhwZXJpZW5jaW5nLiBTb21ldGltZXMgdGFraW5nIHNtYWxsIHN0ZXBzLCBsaWtlIGRvaW5nIHNvbWV0aGluZyB5b3UgZW5qb3kgb3IganVzdCBnZXR0aW5nIG91dHNpZGUgZm9yIGEgc2hvcnQgd2FsaywgY2FuIG1ha2UgYSBkaWZmZXJlbmNlLiBJ4oCZbSBoZXJlIGZvciB5b3XigJRkbyB5b3Ugd2FudCB0byB0YWxrIG1vcmUgYWJvdXQgd2hhdOKAmXMgYmVlbiBvbiB5b3VyIG1pbmQ/In0seyJ0ZXh0IjoiaW5wdXQ6IEkgbWlzcyBob21lIHNvIG11Y2guIEkgdGhvdWdodCBJIHdvdWxkIGFkanVzdCB0byBiZWluZyBhd2F5LCBidXQgSSBmZWVsIG1vcmUgaG9tZXNpY2sgZXZlcnkgZGF5LiJ9LHsidGV4dCI6Im91dHB1dDogSSdtIHJlYWxseSBzb3JyeSB5b3UncmUgZmVlbGluZyBob21lc2ljay4gSXTigJlzIG5hdHVyYWwgdG8gbWlzcyBob21lLCBlc3BlY2lhbGx5IHdoZW4geW91J3JlIGFkanVzdGluZyB0byBhIG5ldyBlbnZpcm9ubWVudC4gU29tZXRpbWVzIHN0YXlpbmcgY29ubmVjdGVkIHdpdGggZmFtaWx5IGFuZCBmcmllbmRzIGZyb20gaG9tZSwgbGlrZSBzY2hlZHVsaW5nIHJlZ3VsYXIgY2FsbHMsIGNhbiBoZWxwIHlvdSBmZWVsIG1vcmUgZ3JvdW5kZWQuIEhhdmUgeW91IGhhZCB0aGUgY2hhbmNlIHRvIGV4cGxvcmUgdGhpbmdzIGFyb3VuZCB5b3VyIG5ldyBhcmVhIHRoYXQgY291bGQgbWFrZSBpdCBmZWVsIG1vcmUgbGlrZSBob21lPyJ9LHsidGV4dCI6ImlucHV0OiBJIGZlZWwgZXhoYXVzdGVkIGFsbCB0aGUgdGltZSwgbGlrZSBubyBtYXR0ZXIgaG93IG11Y2ggSSByZXN0LCBJIGNhbid0IGdldCBteSBlbmVyZ3kgYmFjay4gSSB0aGluayBJJ20gYnVybnQgb3V0LiJ9LHsidGV4dCI6Im91dHB1dDogSSdtIHJlYWxseSBzb3JyeSB5b3UncmUgZmVlbGluZyB0aGlzIHdheS4gQnVybm91dCBjYW4gaGFwcGVuIHdoZW4geW914oCZdmUgYmVlbiBqdWdnbGluZyBhIGxvdCBmb3IgYSBsb25nIHRpbWUuIEl04oCZcyBpbXBvcnRhbnQgdG8gZ2l2ZSB5b3Vyc2VsZiBwZXJtaXNzaW9uIHRvIHJlc3QgYW5kIHRha2UgY2FyZSBvZiB5b3VyIG1lbnRhbCBhbmQgcGh5c2ljYWwgaGVhbHRoLiBFdmVuIHNob3J0IGJyZWFrcyBvciBkb2luZyBzb21ldGhpbmcgZW5qb3lhYmxlIG1pZ2h0IGhlbHAgcmVjaGFyZ2UgeW91ciBlbmVyZ3kuIEhhdmUgeW91IGNvbnNpZGVyZWQgdGFsa2luZyB0byBzb21lb25lIGFib3V0IHlvdXIgd29ya2xvYWQgb3IgZmluZGluZyB3YXlzIHRvIHNldCBib3VuZGFyaWVzIGZvciB5b3Vyc2VsZj8ifSx7InRleHQiOiJpbnB1dDogSSBjYW7igJl0IGZvY3VzIG9uIGFueXRoaW5nIGFueW1vcmUuIEkgdHJ5IHRvIHN0dWR5LCBidXQgbXkgbWluZCBqdXN0IGtlZXBzIHdhbmRlcmluZy4ifSx7InRleHQiOiJvdXRwdXQ6IEl0IHNvdW5kcyBmcnVzdHJhdGluZyB0byBmZWVsIHRoYXQgd2F5LiBTb21ldGltZXMgd2hlbiBvdXIgbWluZHMgYXJlIG92ZXJsb2FkZWQsIGl0J3MgaGFyZGVyIHRvIGNvbmNlbnRyYXRlLiBJdCBtaWdodCBoZWxwIHRvIHRha2Ugc21hbGwgYnJlYWtzIG9yIHRyeSB0ZWNobmlxdWVzIGxpa2UgdGhlIFBvbW9kb3JvIG1ldGhvZOKAlHdvcmtpbmcgaW4gc2hvcnQgaW50ZXJ2YWxzIHdpdGggYnJlYWtzIGluIGJldHdlZW4uIEhhdmUgeW91IGJlZW4gZ2V0dGluZyBlbm91Z2ggc2xlZXAgYW5kIHRha2luZyBjYXJlIG9mIHlvdXJzZWxmPyBTZWxmLWNhcmUgY2FuIHJlYWxseSBpbXBhY3QgZm9jdXMuIFdoYXQgdXN1YWxseSBoZWxwcyB5b3UgcmVmb2N1cyB3aGVuIHlvdSdyZSBkaXN0cmFjdGVkPyJ9LHsidGV4dCI6ImlucHV0OiBJ4oCZbSBzY2FyZWQgb2YgZmFpbGluZy4gTm8gbWF0dGVyIGhvdyBtdWNoIEkgc3R1ZHksIEkgc3RpbGwgZmVlbCBsaWtlIEnigJltIGdvaW5nIHRvIG1lc3MgdXAuIn0seyJ0ZXh0Ijoib3V0cHV0OiBJdCdzIHVuZGVyc3RhbmRhYmxlIHRvIGZlZWwgdGhhdCB3YXksIGVzcGVjaWFsbHkgd2hlbiB5b3UgY2FyZSBhYm91dCB5b3VyIHJlc3VsdHMuIEJ1dCByZW1lbWJlciwgZmFpbHVyZSBpcyBhIHBhcnQgb2YgbGVhcm5pbmcsIGFuZCBpdCBkb2Vzbid0IGRlZmluZSB5b3VyIHdvcnRoIG9yIGFiaWxpdGllcy4gWW91J3JlIHRyeWluZyB5b3VyIGJlc3QsIGFuZCB0aGF0IGVmZm9ydCBjb3VudHMgZm9yIGEgbG90LiBXb3VsZCB5b3UgbGlrZSB0byB0YWxrIGFib3V0IHdoYXQncyBtYWtpbmcgeW91IGZlZWwgbW9zdCB1bmNlcnRhaW4sIG9yIHNvbWUgd2F5cyB0byBidWlsZCBjb25maWRlbmNlIGluIHlvdXIgcHJlcGFyYXRpb24/In0seyJ0ZXh0IjoiaW5wdXQ6IEkga2VlcCBwdXR0aW5nIG9mZiBteSB3b3JrLCBhbmQgbm93IEnigJltIHdvcnJpZWQgSSB3b27igJl0IGJlIGFibGUgdG8gZmluaXNoIGl0IGFsbC4ifSx7InRleHQiOiJvdXRwdXQ6IFByb2NyYXN0aW5hdGlvbiBjYW4gc25lYWsgdXAgb24gYWxsIG9mIHVzLCBlc3BlY2lhbGx5IHdoZW4gdGFza3MgZmVlbCBvdmVyd2hlbG1pbmcuIFNvbWV0aW1lcyBzdGFydGluZyB3aXRoIHRoZSBzbWFsbGVzdCwgZWFzaWVzdCB0YXNrIGNhbiBidWlsZCBtb21lbnR1bS4gWW91IGNhbiBhbHNvIHRyeSBzZXR0aW5nIGEgdGltZXIgZm9yIGp1c3QgMTAtMTUgbWludXRlcyB0byB3b3JrIG9uIHNvbWV0aGluZ+KAlGl0IG1pZ2h0IGhlbHAgeW91IGdldCBpbnRvIHRoZSBmbG93LiBIb3cgYWJvdXQgd2UgbWFrZSBhIHBsYW4gdG9nZXRoZXIgdG8gZ2V0IHN0YXJ0ZWQ/In0seyJ0ZXh0IjoiaW5wdXQ6IEkgZG9u4oCZdCBmZWVsIGxpa2UgSeKAmW0gZ29vZCBlbm91Z2gsIG5vIG1hdHRlciB3aGF0IEkgZG8uIEV2ZXJ5b25lIGVsc2Ugc2VlbXMgc28gbXVjaCBtb3JlIGNhcGFibGUgdGhhbiBtZS4ifSx7InRleHQiOiJvdXRwdXQ6IEknbSByZWFsbHkgc29ycnkgeW91J3JlIGZlZWxpbmcgbGlrZSB0aGlzLiBJdCdzIHRvdWdoIHdoZW4gd2UgY29tcGFyZSBvdXJzZWx2ZXMgdG8gb3RoZXJzLCBidXQgcmVtZW1iZXIsIGV2ZXJ5b25lIGhhcyB0aGVpciBvd24gc3RydWdnbGVzIHRoYXQgYXJlbid0IGFsd2F5cyB2aXNpYmxlLiBZb3XigJlyZSBjYXBhYmxlIGluIHlvdXIgb3duIHdheSwgYW5kIHlvdXIgam91cm5leSBpcyB1bmlxdWUuIFdvdWxkIHlvdSBsaWtlIHRvIHRhbGsgYWJvdXQgd2hhdOKAmXMgYmVlbiBtYWtpbmcgeW91IGZlZWwgdGhpcyB3YXk/IEnigJltIGhlcmUgdG8gbGlzdGVuLiJ9LHsidGV4dCI6ImlucHV0OiBpbSBzdHJlc3NlZCBhYm91dCBub3QgZ2V0dGluZyBnb29kIGdyYWRlcyBpbiBteSBtaWRzZW0gZXhhbXMgdGhhdCBpIHdyb3RlLiBjYW4gd2UgYnJhaW5zdG9ybSBzb21lIHdheXMgdG8gbWFuYWdlIGl0In0seyJ0ZXh0Ijoib3V0cHV0OiAifV19XQ==' # @param {isTemplate: true}
    generation_config_b64 = 'eyJ0ZW1wZXJhdHVyZSI6MSwidG9wX3AiOjAuOTUsInRvcF9rIjo2NCwibWF4X291dHB1dF90b2tlbnMiOjgxOTJ9' # @param {isTemplate: true}
    safety_settings_b64 = "e30="  # @param {isTemplate: true}

    gais_contents = json.loads(base64.b64decode(contents_b64))

    generation_config = json.loads(base64.b64decode(generation_config_b64))
    safety_settings = json.loads(base64.b64decode(safety_settings_b64))

    stream = False
    generation_config = {
        'temperature': 0.8,
        'top_p': 0.95,
        'top_k': 64,
        'max_output_tokens': 8192
    }
    
    # Call the Google API
    response = gemini.generate_content(
            user_input,
            generation_config=generation_config,
            safety_settings=safety_settings,
            stream=False,
        )
    if response and response._result and response._result.candidates:
        candidate = response._result.candidates[0]
        if candidate and candidate.content and candidate.content.parts:
            raw_text = candidate.content.parts[0].text
            
            # Parse and format the text appropriately
            output_text = "<div class='ai-response'>"
            lines = raw_text.split('\n')
            
            for line in lines:
                # Handle lines starting with '*'
                if line.startswith('*'):
                    # Check for bold markers (i.e., **text**)
                    if '**' in line:
                        # Extract text that should be bold
                        parts = line.split('**')
                        list_item = ""
                        for i, part in enumerate(parts):
                            if i % 2 == 1:  # Bold only the parts at odd indices
                                list_item += f"<strong>{part.strip()}</strong>"
                            else:
                                list_item += f"{part.strip()}"
                        output_text += f"<li>{list_item}</li>"
                    else:
                        output_text += f"<li>{line[2:].strip()}</li>"
                elif line.startswith('#'):
                    output_text += f"<h3>{line[1:].strip()}</h3>"
                else:
                    output_text += f"<p>{line}</p>"
            
            output_text += "</div>"
        else:
            output_text = "No valid content in response"
    else:
        output_text = "No response from API"


    save_chat_history(user_input, output_text)
    
    chat_history = load_chat_history()

    return render_template('index.html', chat_history=chat_history)

def save_chat_history(user_input, output_text):
    chat_entry = {
        "user": user_input,
        "ai": output_text
    }
    
    # Load existing history
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, 'r') as f:
            chat_history = json.load(f)
    else:
        chat_history = []
    
    # Append new entry
    chat_history.append(chat_entry)
    
    # Save back to file
    with open(CHAT_HISTORY_FILE, 'w') as f:
        json.dump(chat_history, f)

def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, 'r') as f:
            chat_history = json.load(f)
        return chat_history
    return []

if __name__ == '__main__':
    app.run(debug=True)
