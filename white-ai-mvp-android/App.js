import React, { useRef, useState } from "react";
import {
  ActivityIndicator, KeyboardAvoidingView, Platform, SafeAreaView,
  ScrollView, StatusBar, StyleSheet, Text, TextInput, TouchableOpacity, View
} from "react-native";
import { StatusBar as ExpoStatusBar } from "expo-status-bar";
import { API_BASE_URL } from "./src/config";

export default function App() {
  const [messages, setMessages] = useState([{
    id: "welcome", role: "assistant",
    text: "नमस्ते! यह WHITE AI का शुरुआती Android क्लाइंट है। पहले Backend URL सेट करें।"
  }]);
  const [draft, setDraft] = useState("");
  const [sessionId, setSessionId] = useState(null);
  const [busy, setBusy] = useState(false);
  const scrollRef = useRef(null);

  async function sendMessage() {
    const message = draft.trim();
    if (!message || busy) return;
    if (!API_BASE_URL || API_BASE_URL.includes("YOUR-BACKEND-URL-HERE")) {
      setMessages(prev => [...prev,
        { id: String(Date.now()) + "-user", role: "user", text: message },
        { id: String(Date.now()) + "-config", role: "assistant",
          text: "src/config.js में अपने चल रहे Backend का HTTPS URL सेट करें।" }
      ]);
      setDraft("");
      return;
    }
    setMessages(prev => [...prev, { id: String(Date.now()) + "-user", role: "user", text: message }]);
    setDraft("");
    setBusy(true);
    try {
      const response = await fetch(API_BASE_URL.replace(/\/+$/, "") + "/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, session_id: sessionId })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Backend HTTP " + response.status);
      setSessionId(data.session_id || null);
      setMessages(prev => [...prev, {
        id: String(Date.now()) + "-assistant", role: "assistant",
        text: (data.reply || "खाली उत्तर मिला") +
          (data.note ? "\n\n" + data.note : "") +
          (data.provider ? "\nइंजन: " + data.provider : "")
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        id: String(Date.now()) + "-error", role: "assistant",
        text: "कनेक्शन समस्या: " + error.message + "\nBackend URL और सर्वर स्थिति जाँचें।"
      }]);
    } finally {
      setBusy(false);
    }
  }

  function newChat() {
    setSessionId(null);
    setMessages([{ id: String(Date.now()), role: "assistant", text: "नई चैट शुरू हुई।" }]);
  }

  return (
    <SafeAreaView style={styles.safe}>
      <ExpoStatusBar style="light" />
      <StatusBar barStyle="light-content" backgroundColor="#0b1020" />
      <KeyboardAvoidingView style={styles.flex} behavior={Platform.OS === "ios" ? "padding" : undefined}>
        <View style={styles.header}>
          <View style={styles.logo}><Text style={styles.logoText}>W</Text></View>
          <View style={styles.headerText}>
            <Text style={styles.title}>WHITE AI</Text>
            <Text style={styles.subtitle}>Android क्लाइंट · MVP</Text>
          </View>
          <TouchableOpacity onPress={newChat} style={styles.newChatButton}>
            <Text style={styles.newChatText}>नई चैट</Text>
          </TouchableOpacity>
        </View>
        <View style={styles.notice}>
          <Text style={styles.noticeText}>शुरुआती प्रोटोटाइप। AI API key Backend पर ही रखें। मेमोरी अस्थायी है।</Text>
        </View>
        <ScrollView ref={scrollRef} style={styles.messages} contentContainerStyle={styles.messagesContent}
          onContentSizeChange={() => scrollRef.current?.scrollToEnd({ animated: true })} keyboardShouldPersistTaps="handled">
          {messages.map(item => (
            <View key={item.id} style={[styles.bubble, item.role === "user" ? styles.userBubble : styles.assistantBubble]}>
              <Text style={styles.roleLabel}>{item.role === "user" ? "आप" : "WHITE AI"}</Text>
              <Text style={styles.messageText}>{item.text}</Text>
            </View>
          ))}
          {busy ? <View style={styles.loading}><ActivityIndicator color="#7dd3fc" /><Text style={styles.loadingText}>उत्तर प्राप्त हो रहा है…</Text></View> : null}
        </ScrollView>
        <View style={styles.composer}>
          <TextInput value={draft} onChangeText={setDraft} placeholder="अपना संदेश लिखें…"
            placeholderTextColor="#8794aa" multiline maxLength={4000} style={styles.input} />
          <TouchableOpacity onPress={sendMessage} disabled={busy || !draft.trim()}
            style={[styles.sendButton, (busy || !draft.trim()) && styles.disabledButton]}>
            <Text style={styles.sendText}>{busy ? "रुकें…" : "भेजें"}</Text>
          </TouchableOpacity>
          <Text style={styles.footer}>संवेदनशील जानकारी न भेजें। यह रिलीज़ के लिए तैयार ऐप नहीं है।</Text>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: "#0b1020" },
  flex: { flex: 1 },
  header: { flexDirection: "row", alignItems: "center", paddingHorizontal: 16, paddingTop: 10, paddingBottom: 14, gap: 10 },
  logo: { width: 42, height: 42, borderRadius: 13, backgroundColor: "#7dd3fc", alignItems: "center", justifyContent: "center" },
  logoText: { color: "#07111f", fontSize: 22, fontWeight: "900" },
  headerText: { flex: 1 },
  title: { color: "#f4f7fb", fontSize: 21, fontWeight: "800" },
  subtitle: { color: "#aab6ca", fontSize: 12 },
  newChatButton: { borderColor: "#2b3854", borderWidth: 1, borderRadius: 10, paddingHorizontal: 10, paddingVertical: 8 },
  newChatText: { color: "#f4f7fb", fontWeight: "600", fontSize: 12 },
  notice: { marginHorizontal: 14, marginBottom: 8, borderWidth: 1, borderColor: "#34415c", backgroundColor: "#10182a", borderRadius: 12, padding: 10 },
  noticeText: { color: "#aab6ca", fontSize: 12, lineHeight: 18 },
  messages: { flex: 1 },
  messagesContent: { paddingHorizontal: 14, paddingVertical: 10, gap: 10 },
  bubble: { maxWidth: "92%", borderWidth: 1, borderRadius: 15, padding: 12 },
  userBubble: { alignSelf: "flex-end", backgroundColor: "#17334a", borderColor: "#315775", borderTopRightRadius: 5 },
  assistantBubble: { alignSelf: "flex-start", backgroundColor: "#131b2e", borderColor: "#2b3854", borderTopLeftRadius: 5 },
  roleLabel: { color: "#7dd3fc", fontSize: 11, fontWeight: "800", marginBottom: 5 },
  messageText: { color: "#f4f7fb", fontSize: 15, lineHeight: 22 },
  loading: { flexDirection: "row", alignItems: "center", gap: 8, padding: 8 },
  loadingText: { color: "#aab6ca", fontSize: 12 },
  composer: { paddingHorizontal: 14, paddingTop: 10, paddingBottom: 10, borderTopWidth: 1, borderTopColor: "#1d2940", backgroundColor: "#0b1020" },
  input: { minHeight: 52, maxHeight: 130, borderWidth: 1, borderColor: "#2b3854", borderRadius: 13, backgroundColor: "#10182a", color: "#f4f7fb", paddingHorizontal: 12, paddingVertical: 10, fontSize: 15, textAlignVertical: "top" },
  sendButton: { marginTop: 8, alignItems: "center", justifyContent: "center", borderRadius: 12, paddingVertical: 12, backgroundColor: "#7dd3fc" },
  disabledButton: { opacity: 0.5 },
  sendText: { color: "#07111f", fontWeight: "800" },
  footer: { marginTop: 7, color: "#8794aa", fontSize: 11, textAlign: "center" }
});
