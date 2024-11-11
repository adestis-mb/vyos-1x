<!-- include start from firewall/blacklisting.xml.i -->
<node name="blacklisting">
  <properties>
    <help>Blacklisting configuration</help>
  </properties>
  <children>
    <node name="settings">
      <properties>
        <help>Common blacklisting settings</help>
      </properties>
      <children>
        <node name="abuseipdb">
          <properties>
            <help>AbuseIPDB settings</help>
          </properties>
          <children>
            <leafNode name="key">
              <properties>
                <help>API key for AbuseIPDB</help>
                <constraint>
                  <regex>([A-Za-z0-9]+)</regex>
                </constraint>
              </properties>
            </leafNode>
          </children>
        </node>
      </children>
    </node>
    <tagNode name="group">
      <properties>
        <help>Blacklisting group</help>
        <constraint>
          <regex>[a-zA-Z0-9][\w\-\.]*</regex>
        </constraint>
      </properties>
      <children>
        <node name="scheduling">
          <properties>
            <help>Common blacklisting settings</help>
          </properties>
          <children>
            <tagNode name="task">
              <properties>
                <help>Scheduled task</help>
                <valueHelp>
                  <format>txt</format>
                  <description>Task name</description>
                </valueHelp>
                <priority>999</priority>
              </properties>
              <children>
                <leafNode name="crontab-spec">
                  <properties>
                    <help>UNIX crontab time specification string</help>
                  </properties>
                </leafNode>
                <leafNode name="interval">
                  <properties>
                    <help>Execution interval</help>
                    <valueHelp>
                      <format>&lt;minutes&gt;</format>
                      <description>Execution interval in minutes</description>
                    </valueHelp>
                    <valueHelp>
                      <format>&lt;minutes&gt;m</format>
                      <description>Execution interval in minutes</description>
                    </valueHelp>
                    <valueHelp>
                      <format>&lt;hours&gt;h</format>
                      <description>Execution interval in hours</description>
                    </valueHelp>
                    <valueHelp>
                      <format>&lt;days&gt;d</format>
                      <description>Execution interval in days</description>
                    </valueHelp>
                    <constraint>
                      <regex>[1-9]([0-9]*)([mhd]{0,1})</regex>
                    </constraint>
                  </properties>
                </leafNode>
              </children>
            </tagNode>
          </children>
        </node>
        <node name="sources">
          <properties>
            <help>Common blacklisting settings</help>
          </properties>
          <children>
            <tagNode name="generic-source">
              <properties>
                <help>Scheduled task</help>
                <valueHelp>
                  <format>txt</format>
                  <description>url</description>
                </valueHelp>
                <priority>999</priority>
              </properties>
            </tagNode>
            <node name="abuseipdb">
              <properties>
                <help>AbuseIPDB source</help>
              </properties>
              <children>
                <leafNode name="confidence-level">
                  <properties>
                    <help>AbuseIPDB confidence level</help>
                    <valueHelp>
                      <format>0-100</format>
                      <description>AbuseIPDB confidence level 0-100 (default 70)</description>
                    </valueHelp>
                    <constraint>
                      <validator name="numeric" argument="--range 0-100"/>
                    </constraint>
                    <constraintErrorMessage>AbuseIPDB confidence level must be between 0 and 100</constraintErrorMessage>
                  </properties>
                </leafNode>
              </children>
            </node>
          </children>
        </node>
        <node name="filter">
          <properties>
            <help>Filter results</help>
          </properties>
          <children>
            <tagNode name="network">
              <properties>
                <help>Network name</help>
                <constraint>
                  <regex>[a-zA-Z0-9][\w\-\.]*</regex>
                </constraint>
              </properties>
              <children>
                #include <address-inet.xml.i>
                <tagNode name="firewall-group">
                  <properties>
                    <help>Group name</help>
                    <constraint>
                      <regex>[a-zA-Z0-9][\w\-\.]*</regex>
                    </constraint>
                  </properties>
                </tagNode>
              </children>
            </tagNode>
          </children>
        </node>
        <node name="destination">
          <properties>
            <help>Destination</help>
          </properties>
          <children>
            <tagNode name="file">
              <properties>
                <help>file location</help>
              </properties>
            </tagNode>
            <tagNode name="firewall-group">
              <properties>
                <help>Group name</help>
                <constraint>
                  <regex>[a-zA-Z0-9][\w\-\.]*</regex>
                </constraint>
              </properties>
            </tagNode>
          </children>
        </node>
        <node name="events">
          <properties>
            <help>Events</help>
          </properties>
          <children>
            <node name="before-update">
              <properties>
                <help>Before update</help>
              </properties>
              <children>
                <tagNode name="script">
                  <properties>
                    <help>Script location</help>
                  </properties>
                  <children>
                    <leafNode name="arguments">
                      <properties>
                        <help>Script arguments</help>
                      </properties>
                    </leafNode>
                  </children>
                </tagNode>
              </children>
            </node>
            <node name="after-update">
              <properties>
                <help>Before update</help>
              </properties>
              <children>
                <tagNode name="script">
                  <properties>
                    <help>Script location</help>
                  </properties>
                  <children>
                    <leafNode name="arguments">
                      <properties>
                        <help>Script arguments</help>
                      </properties>
                    </leafNode>
                  </children>
                </tagNode>
              </children>
            </node>
          </children>
        </node>
      </children>
    </tagNode>
  </children>
</node>
<!-- include end -->
