import 'package:mqtt_client/mqtt_client.dart';
import 'package:flutter/material.dart';
import 'package:english_words/english_words.dart';



final MqttClient client = MqttClient('130.113.129.17', '');
Future<void> main() async {
  client.logging(on: true);
  client.onConnected = onConnected;
  final MqttConnectMessage connMess = MqttConnectMessage()
      .withClientIdentifier('Mqtt_MyClientUniqueId');
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
  const String topic2 = 'Team28/TempWarning'; // Not a wildcard topic
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
      title: 'Cardio-Safe',
      theme: new ThemeData(          // Add the 3 lines from here...
        primaryColor: Colors.red,
      ),
      home: SensorInfo(),
    );
  }
// #enddocregion build
}
// #enddocregion MyApp

// #docregion RWS-var
class SensorInfoState extends State<SensorInfo> {
  final _suggestions = <WordPair>[];
  final _saved = new Set<WordPair>();
  final _biggerFont = const TextStyle(fontSize: 36.0);
  final _smallerFont = const TextStyle(fontSize: 24.0);
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
//  String _TempWarning = "";
  // #enddocregion RWS-var

  // #docregion _buildSuggestions
  Widget _buildSuggestions() {
    return new SingleChildScrollView(
        child:Column(children: <Widget>[
          new Text("Welcome to Cardio-Safe",
            style: _biggerFont,
          ),

          GridView.count(
            primary: false,
            crossAxisCount: 3,
            childAspectRatio: 1.6,
            mainAxisSpacing: 1.0,
            crossAxisSpacing: 1.0,
            children: <Widget>[
              new GridTile(child: new Card(
                color: Colors.blue.shade200,
                child: new Center(
                  child: new Text("Sensor"),
                ),
                margin: EdgeInsets.all(0.0),
              ),) ,
              new GridTile(child: new Card(
                  color: Colors.blue.shade200,
                  child: new Center(
                    child: new Text("Reading"),
                  ),
                  margin: EdgeInsets.all(0.0)
              ),) ,
              new GridTile(child: new Card(
                  color: Colors.blue.shade200,
                  child: new Center(
                    child: new Text("Warning"),
                  ),
                  margin: EdgeInsets.all(0.0)
              ),) ,
              new GridTile(child: new Card(
                  color: Colors.blue.shade200,
                  child: new Center(
                    child: new Text("Temperature Sensor (Degrees Celsius)"),
                  ),
                  margin: EdgeInsets.all(0.0)
              ),) ,
              new GridTile(child: new Card(
                  color: Colors.blue.shade200,
                  child: new Center(
                    child: new Text(_msg),
                  ),
                  margin: EdgeInsets.all(0.0)
              ),),
              new GridTile(child: new Card(
                  color: Colors.blue.shade200,
                  child: new Center(
                    child: new Text(_msg2),
                  ),
                  margin: EdgeInsets.all(0.0)
              ),),
              new GridTile(child: new Card(
                  color: Colors.blue.shade200,
                  child: new Center(
                    child: new Text("Heart Rate Sensor (BPM)"),
                  ),
                  margin: EdgeInsets.all(0.0)
              ),),
              new GridTile(child: new Card(
                  color: Colors.blue.shade200,
                  child: new Center(
                    child: new Text(_msg5),
                  ),
                  margin: EdgeInsets.all(0.0)
              ),),
              new GridTile(child: new Card(
                  color: Colors.blue.shade200,
                  child: new Center(
                    child: new Text(_msg6),
                  ),
                  margin: EdgeInsets.all(0.0)
              ),),
              new GridTile(child: new Card(
                  color: Colors.blue.shade200,
                  child: new Center(
                    child: new Text("SPO2 Sensor (%)"),
                  ),
                  margin: EdgeInsets.all(0.0)
              ),),
              new GridTile(child: new Card(
                  color: Colors.blue.shade200,
                  child: new Center(
                    child: new Text(_msg8),
                  ),
                  margin: EdgeInsets.all(0.0)
              ),),
              new GridTile(child: new Card(
                  color: Colors.blue.shade200,
                  child: new Center(
                    child: new Text(_msg9),
                  ),
                  margin: EdgeInsets.all(0.0)
              ),)
            ], //new Cards()
            shrinkWrap: true,
          )
        ],)
    );
//      ListView.builder(
//        padding: const EdgeInsets.all(16.0),
//        itemBuilder: /*1*/ (context, i) {
//          if (i.isOdd) return Divider(); /*2*/
//
//          final index = i ~/ 2; /*3*/
//          if (index >= _suggestions.length) {
//            _suggestions.addAll(generateWordPairs().take(10)); /*4*/
//          }
//          return _buildRow(_suggestions[index]);
//        });
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
        title: Text("CardioSafe"),
        actions: <Widget>[ // Add 3 lines from here...
//            new IconButton(icon: const Icon(Icons.list)),
//          new IconButton(icon: const Icon(Icons.list), onPressed: _pushSaved),
//          new IconButton(icon: const Icon(Icons.list)),
        ],
      ),
      body: _buildSuggestions(),
        drawer: Drawer(
          // Add a ListView to the drawer. This ensures the user can scroll
          // through the options in the Drawer if there isn't enough vertical
          // space to fit everything.
            child: ListView(
              // Important: Remove any padding from the ListView.
              padding: EdgeInsets.zero,
              children: <Widget>[
                DrawerHeader(
                  child: Text('Cardio-Safe',
                    style: _smallerFont,
                  ),
                  decoration: BoxDecoration(
                    color: Colors.red,
                  ),
                ),
                ListTile(
                  title: Text('Home',
                    style: _smallerFont,
                  ),
                  onTap: () {
                    // Update the state of the app
                    // ...
                    // Then close the drawer
                    Navigator.pop(context);
                  },
                ),
                ListTile(
                  title: Text('Graphs',
                    style: _smallerFont,
                  ),
                  onTap: () {
                    // Update the state of the app
                    // ...
                    // Then close the drawer
                    Navigator.pop(context);
                  },
                ),
              ],
            )
        )
    );
  }

//  void _pushSaved() {
//    Navigator.of(context).push(
//      new MaterialPageRoute<void>(   // Add 20 lines from here...
//        builder: (BuildContext context) {
//          final Iterable<ListTile> tiles = _saved.map(
//                (WordPair pair) {
//              return new ListTile(
//                title: new Text(
//                  pair.asPascalCase,
//                  style: _biggerFont,
//                ),
//              );
//            },
//          );
//          final List<Widget> divided = ListTile
//              .divideTiles(
//            context: context,
//            tiles: tiles,
//          )
//              .toList();
//
//          return new Scaffold(         // Add 6 lines from here...
//            appBar: new AppBar(
//              title: Text(_msg2),
//            ),
//            body: new ListView(children: divided),
//          );
//        },
//      ),
//    );
//  }

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
          case 'Team28/TempWarning' : {
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
//        if (_msg2 == "" && _msg3 != "") {
//          _TempWarning = (_msg3);
//        }
//        else if (_msg2 != "" && _msg3 == "") {
//          _TempWarning = (_msg2);
//        }
//        else {
//          _TempWarning = "";
//        }
      });
    });
  }
// #enddocregion RWS-build
// #docregion RWS-var
}
// #enddocregion RWS-var

class SensorInfo extends StatefulWidget {
  @override
  SensorInfoState createState() => new SensorInfoState();

}