
import 'package:mqtt_client/mqtt_client.dart';
import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:english_words/english_words.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'dart:convert' show utf8;


final MqttClient client = MqttClient('130.113.129.17', '');
Future<void> main() async {
  client.logging(on: false);
  client.onConnected = onConnected;
  final MqttConnectMessage connMess = MqttConnectMessage()
      .withClientIdentifier('Mqtt_MyClientUniqueId')
      .keepAliveFor(20) // Must agree with the keep alive set above or not set
      .startClean() // Non persistent session for testing
      .withWillQos(MqttQos.atLeastOnce);
  print('EXAMPLE::Mosquitto client connecting....');
  client.connectionMessage = connMess;
  try {
    await client.connect();
  } on Exception catch (e) {
    print('EXAMPLE::client exception - $e');
    client.disconnect();
  }
  runApp(MyApp());
}

void onConnected(){
  const String topic1 = 'Team28/TempValue'; // Not a wildcard topic
  client.subscribe(topic1, MqttQos.atMostOnce);
  const String topic2 = 'Team28/TempHigh'; // Not a wildcard topic
  client.subscribe(topic2, MqttQos.atMostOnce);
  const String topic3 = 'Team28/TempLow'; // Not a wildcard topic
  client.subscribe(topic3, MqttQos.atMostOnce);
  const String topic4 = 'Team28/TempOutFile'; // Not a wildcard topic
  client.subscribe(topic4, MqttQos.atMostOnce);
  const String topic5 = 'Team28/HRValue'; // Not a wildcard topic
  client.subscribe(topic5, MqttQos.atMostOnce);
  const String topic6 = 'Team28/HRWarning'; // Not a wildcard topic
  client.subscribe(topic6, MqttQos.atMostOnce);
  const String topic7 = 'Team28/HROutFile'; // Not a wildcard topic
  client.subscribe(topic7, MqttQos.atMostOnce);
  const String topic8 = 'Team28/SPO2Value'; // Not a wildcard topic
  client.subscribe(topic8, MqttQos.atMostOnce);
  const String topic9 = 'Team28/SPO2Warning'; // Not a wildcard topic
  client.subscribe(topic9, MqttQos.atMostOnce);
  const String topic10 = 'Team28/SPO2OutFile'; // Not a wildcard topic
  client.subscribe(topic10, MqttQos.atMostOnce);
}

// #docregion MyApp
class MyApp extends StatelessWidget {
  // #docregion build
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Startup Name Generator',
      theme: new ThemeData(          // Add the 3 lines from here...
        primaryColor: Colors.white,
      ),
      home: RandomWords(),
    );
  }
// #enddocregion build
}
// #enddocregion MyApp

// #docregion RWS-var
class RandomWordsState extends State<RandomWords> {
  final _suggestions = <WordPair>[];
  final _saved = new Set<WordPair>();
  final _biggerFont = const TextStyle(fontSize: 18.0);
  String _msg = "";
  String _msg2 = "";
  String _msg3 = "";
  String _msg4 = "";
  String _msg5 = "";
  String _msg6 = "";
  String _msg7 = "";
  String _msg8 = "";
  String _msg9 = "";
  String _msg10 = "";
  // #enddocregion RWS-var

  // #docregion _buildSuggestions
  Widget _buildSuggestions() {
    return ListView.builder(
        padding: const EdgeInsets.all(16.0),
        itemBuilder: /*1*/ (context, i) {
          if (i.isOdd) return Divider(); /*2*/

          final index = i ~/ 2; /*3*/
          if (index >= _suggestions.length) {
            _suggestions.addAll(generateWordPairs().take(10)); /*4*/
          }
          return _buildRow(_suggestions[index]);
        });
  }
  // #enddocregion _buildSuggestions

  // #docregion _buildRow
  Widget _buildRow(WordPair pair) {
    final bool alreadySaved = _saved.contains(pair);
    return new ListTile(
      title: new Text(
        pair.asPascalCase,
        style: _biggerFont,
      ),
      trailing: new Icon(   // Add the lines from here...
        alreadySaved ? Icons.star : Icons.star_border,
        color: alreadySaved ? Colors.red : null,
      ),
      onTap: () {
        setState(() {
          if (alreadySaved) {
            _saved.remove(pair);
          } else {
            _saved.add(pair);
          }
        });
      },               // ... to here.
    );
  }
  // #enddocregion _buildRow

  // #docregion RWS-build
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(_msg),
        actions: <Widget>[      // Add 3 lines from here...
          new IconButton(icon: const Icon(Icons.list), onPressed: _pushSaved),
        ],
      ),
      body: _buildSuggestions(),
    );
  }

  void _pushSaved() {
    Navigator.of(context).push(
      new MaterialPageRoute<void>(   // Add 20 lines from here...
        builder: (BuildContext context) {
          final Iterable<ListTile> tiles = _saved.map(
                (WordPair pair) {
              return new ListTile(
                title: new Text(
                  pair.asPascalCase,
                  style: _biggerFont,
                ),
              );
            },
          );
          final List<Widget> divided = ListTile
              .divideTiles(
            context: context,
            tiles: tiles,
          )
              .toList();

          return new Scaffold(         // Add 6 lines from here...
            appBar: new AppBar(
              title: Text(_msg2),
            ),
            body: new ListView(children: divided),
          );
        },
      ),
    );
  }

  @override
  void initState() {
    super.initState();
    client.updates.listen((List<MqttReceivedMessage<MqttMessage>> c) {
      final MqttPublishMessage recMess = c[0].payload;
      final String pt =
      MqttPublishPayload.bytesToStringAsString(recMess.payload.message);

      this.setState(() {
        switch(c[0].topic){
          case 'Team28/TempValue': {
            _msg = pt;
            break;
          }
          case 'Team28/TempHigh' : {
            _msg2 = pt;
            break;
          }
          case 'Team28/TempLow' : {
            _msg3 = pt;
            break;
          }
          case 'Team28/TempOutFile' : {
            _msg4 = pt;
            break;
          }
          case 'Team28/HRValue' : {
            _msg5 = pt;
            break;
          }
          case 'Team28/HRWarning' : {
            _msg6 = pt;
            break;
          }
          case 'Team28/HROutFile' : {
            _msg7 = pt;
            break;
          }
          case 'Team28/SPO2Value' : {
            _msg8 = pt;
            break;
          }
          case 'Team28/SPO2Warning' : {
            _msg9 = pt;
            break;
          }
          case 'Team28/SPO2OutFile' : {
            _msg10 = pt;
            break;
          }

          default: {
            break;
          }
        }
      });
    });
  }
// #enddocregion RWS-build
// #docregion RWS-var
}
// #enddocregion RWS-var

class RandomWords extends StatefulWidget {
  @override
  RandomWordsState createState() => new RandomWordsState();
}