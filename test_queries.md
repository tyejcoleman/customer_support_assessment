# Test Queries and Expected Outputs

## Overview
Use these test cases to validate your customer support agent implementation. The agent should search the knowledge base (sample_faq.json) first for all queries and only escalate when appropriate.

---

## Category 1: FAQ/Knowledge Base Queries
*These should be answered from the sample_faq.json knowledge base without escalation*

### Query 1: Payment Methods
**Input:** "What payment methods do you accept?"
**Expected Behavior:**
- Agent searches knowledge base
- Returns: "We accept credit cards, debit cards, cash, WeChat Pay, Alipay, and gift cards."
- No escalation needed

### Query 2: Cancellation Policy
**Input:** "Is there a cancellation fee?"
**Expected Behavior:**
- Agent searches knowledge base
- Returns information about 12 hours' notice and 50% cancellation fee
- No escalation needed

### Query 3: Membership Program
**Input:** "How do I become a member?"
**Expected Behavior:**
- Agent searches for membership information
- Returns: Sign up at front desk or online, $39.99/month, includes benefits
- No escalation needed

### Query 4: Birthday Specials
**Input:** "Do you offer birthday specials?"
**Expected Behavior:**
- Agent searches knowledge base
- Returns: "Yes, you receive 20% off one service during your birthday month. Please show a valid ID."
- No escalation needed

### Query 5: Parking Information
**Input:** "Do you have parking available?"
**Expected Behavior:**
- Agent searches for parking information
- Returns: "Yes, we offer free parking and accessible parking spaces."
- No escalation needed

### Query 6: Facilities
**Input:** "Are showers and changing rooms available?"
**Expected Behavior:**
- Agent searches knowledge base
- Returns information about individual changing rooms and showers with amenities
- No escalation needed

### Query 7: Deposit Requirements
**Input:** "Do I need to pay a deposit?"
**Expected Behavior:**
- Agent searches knowledge base
- Returns: Information about deposits for high-demand services
- No escalation needed

---

## Category 2: Escalation Required
*These should trigger human handoff*

### Query 8: Billing Issue
**Input:** "I was charged twice for my membership last month"
**Expected Behavior:**
- Agent recognizes billing/payment issue
- Immediately escalates with reason: "Customer reporting duplicate billing charge"
- Shows handoff notification in CLI

### Query 9: Explicit Human Request
**Input:** "I want to speak to a human agent please"
**Expected Behavior:**
- Agent recognizes explicit request for human
- Escalates with reason: "Customer requested human agent"
- Shows handoff notification

### Query 10: Account Security
**Input:** "Someone else is using my membership account"
**Expected Behavior:**
- Agent recognizes security/account issue
- Immediately escalates with reason: "Account security concern - unauthorized access"
- Shows urgent handoff notification

### Query 11: Refund Request
**Input:** "I want a refund for my service yesterday"
**Expected Behavior:**
- Agent recognizes refund/financial request
- Escalates with reason: "Customer requesting refund"
- Shows handoff notification

### Query 12: Frustrated Customer
**Input:** "This is terrible! I've been waiting for 30 minutes and no one is helping me!"
**Expected Behavior:**
- Agent recognizes frustration/anger
- Apologizes for the experience
- Escalates with reason: "Customer expressing significant frustration - needs immediate assistance"
- Shows handoff notification

### Query 13: Complaint About Service
**Input:** "The service I received was completely unprofessional and I want to file a complaint"
**Expected Behavior:**
- Agent recognizes complaint requiring human intervention
- Escalates with reason: "Customer filing service complaint"
- Shows handoff notification

---

## Category 3: Edge Cases
*Test boundary conditions and error handling*

### Query 14: Information Not in Knowledge Base
**Input:** "What are your hours on holidays?"
**Expected Behavior:**
- Agent searches knowledge base
- Cannot find holiday hours information
- Escalates with reason: "Information not available in knowledge base"

### Query 15: Partial Information Match
**Input:** "Can I pay with Apple Pay?"
**Expected Behavior:**
- Agent searches for payment methods
- Finds general payment info but Apple Pay not specifically mentioned
- Either provides available payment methods or escalates for specific clarification

### Query 16: Multiple Questions
**Input:** "What's your cancellation policy and do you have parking?"
**Expected Behavior:**
- Agent searches knowledge base for both topics
- Provides both answers from knowledge base
- No escalation needed

### Query 17: Clarification Needed
**Input:** "How much does it cost?"
**Expected Behavior:**
- Agent asks for clarification: "I'd be happy to help with pricing. Are you asking about membership costs or a specific service?"
- Based on response, searches knowledge base or escalates

### Query 18: Modified Question
**Input:** "What forms of payment are accepted?"
**Expected Behavior:**
- Agent recognizes this is similar to "What payment methods do you accept?"
- Searches and finds payment information
- Returns correct answer from knowledge base

---

## Category 4: Conversation Flow Tests

### Query 19: Greeting
**Input:** "Hello"
**Expected Behavior:**
- Agent responds with professional greeting
- Asks how they can help
- No immediate search or escalation

### Query 20: Thank You
**Input:** "Thank you, that answered my question!"
**Expected Behavior:**
- Agent acknowledges resolution
- Asks if there's anything else needed
- No escalation

### Query 21: Follow-up Question
**Input:** After asking about membership: "Can I cancel anytime?"
**Expected Behavior:**
- Agent searches for membership cancellation terms
- If not in knowledge base, escalates for policy clarification
- Maintains context from previous question

### Query 22: Off-Topic
**Input:** "What's the weather like today?"
**Expected Behavior:**
- Agent politely redirects to support topics
- "I'm here to help with questions about our services. Is there anything specific about our business I can help you with?"
- No escalation

---

## Validation Checklist

### For Each Test Query, Verify:
- [ ] Agent searches knowledge base when appropriate
- [ ] Response matches sample_faq.json content exactly (not hallucinated)
- [ ] Escalation happens for the right reasons
- [ ] Handoff notification displays correctly in CLI
- [ ] Professional tone is maintained
- [ ] Error cases are handled gracefully

### Success Criteria:
- ✅ All FAQ queries answered accurately from sample_faq.json
- ✅ Payment, cancellation, membership questions handled correctly
- ✅ All escalation triggers work correctly
- ✅ Edge cases handled appropriately
- ✅ No information provided that's not in the knowledge base
- ✅ Consistent professional tone

### Common Issues to Watch For:
- ❌ Agent providing information not in sample_faq.json
- ❌ Escalating for questions that ARE in the FAQ
- ❌ Not escalating for billing/security issues
- ❌ Mixing up or combining different FAQ answers
- ❌ Not handling variations of FAQ questions
- ❌ Poor error handling causing crashes

### Testing Tips:
1. Start with exact FAQ questions to verify basic functionality
2. Try rephrased versions of FAQ questions
3. Test all escalation scenarios
4. Verify the agent doesn't hallucinate extra information
5. Check that responses match sample_faq.json content exactly